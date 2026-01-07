/**
 * Google Apps Script for ShramTools Contact Form
 * 
 * SETUP INSTRUCTIONS:
 * 
 * 1. Create a new Google Sheet for storing contact form submissions
 * 2. Go to Extensions > Apps Script
 * 3. Delete any existing code and paste this entire script
 * 4. Replace 'YOUR_SHEET_NAME' with your actual sheet name (or leave as 'Submissions')
 * 5. Save the script (File > Save or Ctrl/Cmd + S)
 * 6. Click "Deploy" > "New deployment"
 * 7. Click the gear icon next to "Select type" and choose "Web app"
 * 8. Set the following:
 *    - Description: "ShramTools Contact Form"
 *    - Execute as: "Me"
 *    - Who has access: "Anyone"
 * 9. Click "Deploy"
 * 10. Copy the Web App URL
 * 11. Paste the URL in contact.html where it says 'YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL_HERE'
 * 12. Authorize the script when prompted
 * 
 * The script will automatically:
 * - Create headers in your sheet if they don't exist
 * - Store all form submissions with timestamp
 * - Send auto-reply email to the user (optional - configure below)
 * - Send notification email to you (optional - configure below)
 */

// ============= CONFIGURATION =============

// Sheet name where data will be stored
const SHEET_NAME = 'Submissions';

// Your email address for notifications (set to null to disable)
const NOTIFICATION_EMAIL = 'your-email@example.com'; // Change this to your email

// Enable/disable auto-reply to users
const SEND_AUTO_REPLY = true; // Set to false to disable

// Auto-reply email template
const AUTO_REPLY_SUBJECT = 'Thank you for contacting ShramTools';
const AUTO_REPLY_BODY = `
Dear {name},

Thank you for contacting ShramTools!

We have received your message regarding: {subject}

Our team will review your inquiry and get back to you as soon as possible.

Your Inquiry Details:
- Type: {inquiryType}
- Subject: {subject}
- Tool Name: {toolName}

If you have any additional information to share, please feel free to reply to this email.

Best regards,
The ShramTools Team
https://shramtools.shramkavach.com
`;

// ============= MAIN FUNCTIONS =============

/**
 * Handle POST requests from the contact form
 */
function doPost(e) {
  try {
    // Check if request has data
    if (!e || !e.postData || !e.postData.contents) {
      throw new Error('No data received');
    }
    
    // Parse the incoming data
    let data;
    try {
      data = JSON.parse(e.postData.contents);
    } catch (parseError) {
      // Try to parse as URL-encoded data
      data = parseFormData(e);
    }
    
    // Validate required fields
    if (!data.name || !data.email || !data.subject) {
      throw new Error('Missing required fields');
    }
    
    // Get or create the spreadsheet sheet
    const sheet = getOrCreateSheet();
    
    // Add data to sheet
    addDataToSheet(sheet, data);
    
    // Send notification email to admin
    if (NOTIFICATION_EMAIL && NOTIFICATION_EMAIL !== 'your-email@example.com') {
      sendNotificationEmail(data);
    }
    
    // Send auto-reply to user
    if (SEND_AUTO_REPLY && data.email) {
      sendAutoReply(data);
    }
    
    // Return success response
    return ContentService.createTextOutput(JSON.stringify({
      status: 'success',
      message: 'Form submitted successfully'
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    // Log error with details
    Logger.log('Error processing form: ' + error.toString());
    if (e && e.postData) {
      Logger.log('Post data: ' + e.postData.contents);
    }
    
    // Return error response
    return ContentService.createTextOutput(JSON.stringify({
      status: 'error',
      message: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Parse form data from URL-encoded format
 */
function parseFormData(e) {
  const data = {};
  if (e.parameter) {
    Object.keys(e.parameter).forEach(key => {
      data[key] = e.parameter[key];
    });
  }
  return data;
}

/**
 * Handle GET requests (for testing)
 */
function doGet(e) {
  const html = `
    <html>
      <body>
        <h1>ShramTools Contact Form API</h1>
        <p>Status: ✅ Running</p>
        <p>This Web App is ready to receive contact form submissions.</p>
        <hr>
        <h2>Test the API</h2>
        <button onclick="testAPI()">Send Test Submission</button>
        <div id="result"></div>
        <script>
          function testAPI() {
            const testData = {
              name: 'Test User',
              email: 'test@example.com',
              inquiryType: 'General Question / Support',
              subject: 'Test Submission',
              message: 'This is a test message.',
              toolName: 'Test Tool',
              timestamp: new Date().toISOString()
            };
            
            fetch(window.location.href, {
              method: 'POST',
              body: JSON.stringify(testData)
            })
            .then(response => response.text())
            .then(data => {
              document.getElementById('result').innerHTML = '<pre>' + data + '</pre>';
            })
            .catch(error => {
              document.getElementById('result').innerHTML = '<p style="color:red;">Error: ' + error + '</p>';
            });
          }
        </script>
      </body>
    </html>
  `;
  
  return HtmlService.createHtmlOutput(html);
}

/**
 * Get existing sheet or create new one with headers
 */
function getOrCreateSheet() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = spreadsheet.getSheetByName(SHEET_NAME);
  
  // Create sheet if it doesn't exist
  if (!sheet) {
    sheet = spreadsheet.insertSheet(SHEET_NAME);
  }
  
  // Add headers if sheet is empty
  if (sheet.getLastRow() === 0) {
    const headers = [
      'Timestamp',
      'Name',
      'Email',
      'Inquiry Type',
      'Subject',
      'Message',
      'Tool Name',
      'Status'
    ];
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    
    // Format header row
    sheet.getRange(1, 1, 1, headers.length)
      .setFontWeight('bold')
      .setBackground('#667eea')
      .setFontColor('#ffffff');
    
    // Freeze header row
    sheet.setFrozenRows(1);
    
    // Auto-resize columns
    for (let i = 1; i <= headers.length; i++) {
      sheet.autoResizeColumn(i);
    }
  }
  
  return sheet;
}

/**
 * Add form data to sheet
 */
function addDataToSheet(sheet, data) {
  const timestamp = new Date();
  const row = [
    timestamp,
    data.name || '',
    data.email || '',
    data.inquiryType || '',
    data.subject || '',
    data.message || '',
    data.toolName || '',
    'New'
  ];
  
  sheet.appendRow(row);
  
  // Auto-resize columns after adding data
  const lastColumn = sheet.getLastColumn();
  for (let i = 1; i <= lastColumn; i++) {
    sheet.autoResizeColumn(i);
  }
}

/**
 * Send notification email to admin
 */
function sendNotificationEmail(data) {
  try {
    const subject = `New Contact Form Submission: ${data.inquiryType}`;
    const body = `
You have received a new contact form submission on ShramTools.

==== Contact Details ====
Name: ${data.name}
Email: ${data.email}

==== Inquiry Details ====
Type: ${data.inquiryType}
Subject: ${data.subject}
Tool Name: ${data.toolName || 'N/A'}

==== Message ====
${data.message}

==== Timestamp ====
${new Date().toLocaleString()}

---
This is an automated notification from ShramTools Contact Form.
View all submissions: ${SpreadsheetApp.getActiveSpreadsheet().getUrl()}
    `;
    
    MailApp.sendEmail({
      to: NOTIFICATION_EMAIL,
      subject: subject,
      body: body
    });
  } catch (error) {
    console.error('Error sending notification email:', error);
  }
}

/**
 * Send auto-reply email to user
 */
function sendAutoReply(data) {
  try {
    // Replace placeholders in template
    let body = AUTO_REPLY_BODY
      .replace('{name}', data.name)
      .replace('{subject}', data.subject)
      .replace(/{subject}/g, data.subject)
      .replace('{inquiryType}', data.inquiryType)
      .replace('{toolName}', data.toolName || 'N/A');
    
    MailApp.sendEmail({
      to: data.email,
      subject: AUTO_REPLY_SUBJECT,
      body: body
    });
  } catch (error) {
    console.error('Error sending auto-reply:', error);
  }
}

/**
 * Test function - run this to test the setup
 */
function testSetup() {
  const testData = {
    name: 'Test User',
    email: 'test@example.com',
    inquiryType: 'Bug Report / Technical Issue',
    subject: 'Test Submission',
    message: 'This is a test message to verify the setup.',
    toolName: 'Mortgage Calculator',
    timestamp: new Date().toISOString()
  };
  
  const sheet = getOrCreateSheet();
  addDataToSheet(sheet, testData);
  
  Logger.log('Test completed! Check your spreadsheet.');
}
