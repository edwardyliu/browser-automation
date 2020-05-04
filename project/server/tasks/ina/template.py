# project/server/tasks/ina/template.py

# == Import(s) ==
# => System
import datetime

# == E-mail Template ==
# => Plain-text version
text = lambda status: """\
Nauto Report:

Dear Valued Customer,
  The task is complete. The resulting CSV file is attached.
  Task Status: Success
""" if status else """\
Nauto Report:

Dear Valued Customer,
  The task is complete. The resulting CSV file is attached.
  Task Status: Failure
"""

# => HTML version
header = """\
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Nauto Report</title>
  <style>
  .task-box {
    max-width: 800px;
    margin: auto;
    padding: 30px;
    border: 1px solid #eee;
    box-shadow: 0 0 10px rgba(0, 0, 0, .15);
    font-size: 1.0em;
    line-height: 1.5em;
    font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
    color: #555;
  }
  .task-box table {
    width: 100%;
    line-height: inherit;
    text-align: left;
  }
  .task-box table td {
    padding: 5px;
    vertical-align: top;
  }
  .task-box table tr td:nth-child(3) {
    text-align: right;
  }
  .task-box table tr.top table td {
    padding-bottom: 20px;
  }
  .task-box table tr.top table td.title {
    font-size: 5.5em;
    line-height: 1.0em;
    color: #333;
  }
  .task-box table tr.information table td {
    padding-bottom: 40px;
  }
  .task-box table tr.heading td {
    background: #eee;
    border-bottom: 1px solid #ddd;
    font-weight: bold;
  }
  .task-box table tr.details td {
    padding-bottom: 20px;
  }
  .task-box table tr.item td{
    border-bottom: 1px solid #eee;
  }
  .task-box table tr.item.last td {
    border-bottom: none;
  }
  .task-box table tr.summary td:nth-child(3) {
    border-top: 2px solid #eee;
  }
  @media only screen and (max-width: 600px) {
    .task-box table tr.top table td {
      width: 100%;
      display: block;
      text-align: center;
    }
    .task-box table tr.information table td {
      width: 100%;
      display: block;
      text-align: center;
    }
  }

  /** RTL **/
  .rtl {
    direction: rtl;
    font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
  }
  .rtl table {
    text-align: right;
  }
  .rtl table {
    text-align: right;
  }
  .rtl table tr td:nth-child(3) {
    text-align: left;
  }
  </style>
</head>
<body>
  <div class="task-box">
    <table cellpadding="0" cellspacing="0">\n
"""

body_meta = lambda taskid, dt: f"""\
      <!-- Metadata: Task ID, Date, Enqueue & Dequeue Time -->
      <tr class="top">
        <td colspan="3">
          <table>
            <tr>
              <td class="title">
                <span style="color: #010100;">N</span><span style="color: #FD7F20;">a</span><span style="color: #4d4d4d;">u</span><span style="color: #FC2E20;">to</span>
              </td>
              <td></td>
              <td>
                <span style="font-weight: bold;">Date:</span> {dt.strftime("%B %d, %Y")}<br>
                <span style="font-weight: bold;">Open:</span> <span style="font-style: italic;">T</span>{dt.strftime("%H:%M:%S")}<br>
                <span style="font-weight: bold;">Close:</span> <span style="font-style: italic;">T</span>{datetime.datetime.now().strftime("%H:%M:%S")}<br>
                <span style="font-weight: bold;">Nauto Task ID:</span><br>
                <span style="font-style: italic; font-size: 0.7em;">{taskid}</span>
              </td>
            </tr>
          </table>
        </td>
      </tr>\n
"""

body_information = lambda email: f"""\
      <!-- Information: Sender -->
      <tr class="information">
        <td colspan="3">
          <table>
            <tr>
              <td>
                EdwardLiu, Inc.<br>
                123 Maven Road<br>
                Mavenville, ON A1B2C3
              </td>
              <td></td>
              <td>
                ABC Corp.<br>
                Edward Liu<br>
                <a href="mailto:{email}">{email}</a>
              </td>
            </tr>
          </table>
        </td>
      </tr>\n
"""

body_content_head = lambda i,j,k: f"""\
      <!-- Content Head -->
      <tr class="heading">
        <td>{i}</td>
        <td>{j}</td>
        <td>{k}</td>
      </tr>

      <!-- Content Items -->\n
"""

body_content_item = lambda i,j,k,last: f"""\
      <tr class="item last">
          <td>{i}</td>
          <td>{j}</td>
          <td>{k}</td>
      </tr>\n
""" if last else f"""\
      <tr class="item">
          <td>{i}</td>
          <td>{j}</td>
          <td>{k}</td>
      </tr>\n
"""

body_content_summary = lambda status: """\
      <!-- Content Summary -->
      <tr class="summary">
        <td></td>
        <td></td>
        <td>
          Status: <span style="color: #009900; font-weight: bold;">Success</span><br>
        </td>
      </tr>\n
""" if status else """\
      <!-- Content Summary -->
      <tr class="summary">
        <td></td>
        <td></td>
        <td>
          Status: <span style="color: #d10000; font-weight: bold;">Failure</span>
        </td>
      </tr>\n
"""

footer = lambda email: f"""\
    </table>
    
    <!-- Footer -->
    <table width="640" cellspacing="0" cellpadding="0" border="0" align="center" style="max-width:640px; width:100%;" bgcolor="#FFFFFF">
      <tr>
        <td align="center" valign="top" style="padding:10px;">
          <table width="600" cellspacing="0" cellpadding="0" border="0" align="center" style="max-width:600px; width:100%;">
            <tr>
              <td align="center" valign="top" style="padding:10px; font-family: 'Open Sans', sans-serif; font-size: 0.75em;">
                Notice something wrong?<br>
                Please <a href="mailto:{email}">contact our support team</a> and we'll be happy to help.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </div>
</body>
</html>
"""