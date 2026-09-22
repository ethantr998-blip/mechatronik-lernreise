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

    ws.onmessage = (evt) => {
      const data = JSON.parse(evt.data);
      if (data.id && callbacks.has(data.id)) {
        callbacks.get(data.id)(data.result);
        callbacks.delete(data.id);
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
    await wait(4000);

    // Step 1: Set Year to 2026 (2026 - 2027) and trigger postback if needed
    console.log('Setting Year to 2026...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const ddlYear = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_uYearSemester1_ddlYearID");
        for (let i = 0; i < ddlYear.options.length; i++) {
          if (ddlYear.options[i].text.includes("2026 - 2027") || ddlYear.options[i].value === "2026") {
            ddlYear.selectedIndex = i;
            ddlYear.dispatchEvent(new Event("change", { bubbles: true }));
            break;
          }
        }
      })()`
    });
    await wait(3000);

    // Step 2: Set Khoa to Kỹ thuật công nghệ
    console.log('Setting Khoa to Kỹ thuật công nghệ...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const ddlSci = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_UClass1_ddlScienceID");
        if (ddlSci) {
          for (let i = 0; i < ddlSci.options.length; i++) {
            if (ddlSci.options[i].text.includes("Kỹ thuật công nghệ")) {
              ddlSci.selectedIndex = i;
              ddlSci.dispatchEvent(new Event("change", { bubbles: true }));
              break;
            }
          }
        }
      })()`
    });
    await wait(3000);

    // Step 3: Set Khoá to Cao đẳng K20
    console.log('Setting Khoá to Cao đẳng K20...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const ddlCourse = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_UClass1_ddlCourseID");
        if (ddlCourse) {
          for (let i = 0; i < ddlCourse.options.length; i++) {
            if (ddlCourse.options[i].text.includes("Cao đẳng K20")) {
              ddlCourse.selectedIndex = i;
              ddlCourse.dispatchEvent(new Event("change", { bubbles: true }));
              break;
            }
          }
        }
      })()`
    });
    await wait(3000);

    // Step 4: Set Week to Tuần 13 (21/09 - 27/09)
    console.log('Setting Week to Tuần 13 (21/09 - 27/09)...');
    const weekInfo = await send('Runtime.evaluate', {
      expression: `(() => {
        const ddlWeek = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_ddlWeek");
        const list = [];
        if (ddlWeek) {
          for (let i = 0; i < ddlWeek.options.length; i++) {
            list.push({ idx: i, val: ddlWeek.options[i].value, text: ddlWeek.options[i].text });
            if (ddlWeek.options[i].text.includes("21/09") || ddlWeek.options[i].text.includes("Tuần 13")) {
              ddlWeek.selectedIndex = i;
              ddlWeek.dispatchEvent(new Event("change", { bubbles: true }));
            }
          }
        }
        return list.slice(10, 16);
      })()`,
      returnByValue: true
    });
    console.log('Weeks nearby:', weekInfo.result.value);
    await wait(1000);

    // Step 5: Set Class to Cơ điện tử- tiêu chuẩn của Đức làm việc tại CHLB Đức 3- Cao đẳng K20
    console.log('Setting Class to Đức 3 K20...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const ddlClass = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_UClass1_ddlClassID");
        if (ddlClass) {
          for (let i = 0; i < ddlClass.options.length; i++) {
            if (ddlClass.options[i].text.includes("CHLB Đức 3") || ddlClass.options[i].text.includes("Đức 3- Cao đẳng K20")) {
              ddlClass.selectedIndex = i;
              ddlClass.dispatchEvent(new Event("change", { bubbles: true }));
              break;
            }
          }
        }
      })()`
    });
    await wait(1000);

    // Step 6: Click "Tìm kiếm"
    console.log('Clicking Tìm kiếm button...');
    await send('Runtime.evaluate', {
      expression: `(() => {
        const btn = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_UClass1_btnSearch");
        if (btn) btn.click();
      })()`
    });
    await wait(5000);

    // Step 7: Extract table and screenshot
    const res = await send('Runtime.evaluate', {
      expression: `(() => {
        const title = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_lblTitle")?.innerText || "";
        const contentElem = document.getElementById("ctl00_cphMain_ScheduleOfClass1_uScheduleOfClass1_lblContent");
        
        const tables = contentElem ? Array.from(contentElem.querySelectorAll("table")) : [];
        const rowsData = [];
        tables.forEach(tbl => {
          const trs = Array.from(tbl.querySelectorAll("tr"));
          trs.forEach(tr => {
            const cells = Array.from(tr.querySelectorAll("th, td")).map(td => td.innerText.replace(/\\s+/g, ' ').trim());
            if (cells.length > 0 && cells.some(c => c.length > 0)) {
              rowsData.push(cells);
            }
          });
        });

        return {
          title,
          rows: rowsData,
          html: contentElem?.innerHTML || "",
          text: contentElem?.innerText || ""
        };
      })()`,
      returnByValue: true
    });

    console.log('=== SEARCH RESULT ===');
    console.log('Title:', res.result.value.title);
    console.log('Rows count:', res.result.value.rows.length);
    console.log('Text content:', res.result.value.text);
    if (res.result.value.rows.length > 0) {
      console.log('Full rows:\n', JSON.stringify(res.result.value.rows, null, 2));
    }

    // Take screenshot to inspect visually
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    const fs = require('fs');
    fs.writeFileSync('/Users/trangiaphat/.gemini/antigravity/brain/ea06d3bd-74bf-4d6a-90ab-7120bce9a1ae/scratch/result_schedule.png', Buffer.from(shot.data, 'base64'));
    console.log('Screenshot saved to scratch/result_schedule.png');

    ws.close();
  } finally {
    browserProc.kill('SIGKILL');
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
