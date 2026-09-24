const { spawn } = require('child_process');

async function wait(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function waitForCDP(port, maxTries = 20) {
  for (let i = 0; i < maxTries; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (res.ok) return await res.json();
    } catch (e) {}
    await wait(500);
  }
  throw new Error('CDP not reachable');
}

async function main() {
  const coccocPath = '/Applications/CocCoc.app/Contents/MacOS/CocCoc';
  const port = 9339;
  const userDataDir = '/tmp/coccoc_tmp_profile_' + Date.now();

  const browserProc = spawn(coccocPath, [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--disable-gpu',
    '--no-sandbox',
    `--user-data-dir=${userDataDir}`,
    'about:blank'
  ], { stdio: 'ignore' });

  try {
    await waitForCDP(port);

    const newTargetRes = await fetch(`http://127.0.0.1:${port}/json/new?https://congthongtin.lilama2.edu.vn/Pages/Sims/ScheduleOfClass.aspx?pt=4`, { method: 'PUT' });
    const target = await newTargetRes.json();

    const ws = new WebSocket(target.webSocketDebuggerUrl);
    let msgId = 1;
    const callbacks = new Map();
    let navigatedResolver = null;

    ws.onmessage = (evt) => {
      const data = JSON.parse(evt.data);
      if (data.id && callbacks.has(data.id)) {
        callbacks.get(data.id)(data.result);
        callbacks.delete(data.id);
      }
      if (data.method === 'Page.loadEventFired' && navigatedResolver) {
        navigatedResolver();
        navigatedResolver = null;
      }
    };

    await new Promise(r => ws.onopen = r);
    const send = (method, params = {}) => {
      return new Promise(resolve => {
        const id = msgId++;
        callbacks.set(id, resolve);
        ws.send(JSON.stringify({ id, method, params }));
      });
    };

    await send('Page.enable');
    await send('Runtime.enable');
    await wait(3000);

    const evalExpr = async (expr) => {
      const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true });
      return r.result?.value;
    };

    const triggerPostBackAndWait = async (code) => {
      const p = new Promise(r => { navigatedResolver = r; });
      await evalExpr(code);
      await Promise.race([p, wait(6000)]);
      await wait(800);
    };

    // Step 1: Set Year to 2026 - 2027 and trigger postback
    console.log('Setting Year to 2026 - 2027...');
    await triggerPostBackAndWait(`(() => {
      const ddl = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_uYearSemester1_ddlYearID");
      ddl.value = "2026";
      if (ddl.onchange) ddl.onchange();
    })()`);

    // Step 2: Set Khoa to Kỹ thuật công nghệ
    console.log('Setting Khoa to Kỹ thuật công nghệ...');
    await triggerPostBackAndWait(`(() => {
      const ddl = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_UClass1_ddlScienceID");
      for (let i = 0; i < ddl.options.length; i++) {
        if (ddl.options[i].text.includes("Kỹ thuật công nghệ")) {
          ddl.selectedIndex = i;
          if (ddl.onchange) ddl.onchange();
          break;
        }
      }
    })()`);

    // Step 3: Set Khoá to Cao đẳng K20
    console.log('Setting Khoá to Cao đẳng K20...');
    await triggerPostBackAndWait(`(() => {
      const ddl = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_UClass1_ddlCourseID");
      for (let i = 0; i < ddl.options.length; i++) {
        if (ddl.options[i].text.includes("Cao đẳng K20")) {
          ddl.selectedIndex = i;
          if (ddl.onchange) ddl.onchange();
          break;
        }
      }
    })()`);

    // Step 4: Set Week to Tuần 13 and Class to 26.02.37.03
    console.log('Selecting Week and Class...');
    await evalExpr(`(() => {
      const ddlWeek = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_ddlWeek");
      for (let i = 0; i < ddlWeek.options.length; i++) {
        if (ddlWeek.options[i].text.includes("21/09") || ddlWeek.options[i].text.includes("Tuần 13")) {
          ddlWeek.selectedIndex = i;
          break;
        }
      }
      const ddlClass = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_UClass1_ddlClassID");
      for (let i = 0; i < ddlClass.options.length; i++) {
        if (ddlClass.options[i].value === "26.02.37.03" || ddlClass.options[i].text.includes("CHLB Đức 3")) {
          ddlClass.selectedIndex = i;
          break;
        }
      }
    })()`);

    // Step 5: Click Tìm kiếm
    console.log('Clicking Tìm kiếm button...');
    await triggerPostBackAndWait(`(() => {
      const btn = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_UClass1_btnSearch");
      if (btn) btn.click();
    })()`);

    // Step 6: Extract table
    const res = await evalExpr(`(() => {
      const title = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_lblTitle")?.innerText || "";
      const contentElem = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_lblContent");
      const tables = contentElem ? Array.from(contentElem.querySelectorAll("table")) : [];
      const rowsData = [];
      tables.forEach(tbl => {
        const trs = Array.from(tbl.querySelectorAll("tr"));
        trs.forEach(tr => {
          const cells = Array.from(tr.querySelectorAll("th, td")).map(td => td.innerText.replace(/\\s+/g, " ").trim());
          if (cells.length > 0 && cells.some(c => c.length > 0)) {
            rowsData.push(cells);
          }
        });
      });
      return { title, rows: rowsData };
    })()`);

    console.log('=== SEARCH RESULT ===');
    console.log('Title:', res.title);
    console.log('Rows count:', res.rows.length);
    console.log('Full rows:\n', JSON.stringify(res.rows, null, 2));

    ws.close();
  } finally {
    browserProc.kill('SIGKILL');
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
