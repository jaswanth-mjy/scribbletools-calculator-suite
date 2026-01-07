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
const NOTIFICATION_EMAIL = 'shramkavach@gmail.com'; // Change this to your email

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
  return handleRequest(e);
}

/**
 * Handle GET requests (also processes form data via URL parameters)
 */
function doGet(e) {
  try {
    // Create a safe event object if undefined
    const safeEvent = e || {};
    
    Logger.log('doGet called');
    Logger.log('Event object type: ' + typeof e);
    Logger.log('Event is null: ' + (e === null));
    Logger.log('Event is undefined: ' + (e === undefined));
    
    // Always try to process as form submission first
    // Apps Script sometimes doesn't pass the event object properly
    return handleRequest(safeEvent);
    
  } catch (error) {
    Logger.log('doGet error: ' + error.toString());
    
    // Show error page
    const html = `
      <html>
        <body>
          <h1>Error</h1>
          <p style="color:red;">There was an error processing your request.</p>
          <p>Error: ${error.toString()}</p>
          <hr>
          <p><a href="https://shramtools.shramkavach.com/contact.html">← Back to Contact Form</a></p>
        </body>
      </html>
    `;
    return HtmlService.createHtmlOutput(html);
  }
}

/**
 * Main request handler for both GET and POST
 */
function handleRequest(e) {
  try {
    Logger.log('handleRequest called');
    Logger.log('Event type: ' + typeof e);
    Logger.log('Event is undefined: ' + (e === undefined));
    Logger.log('Event is null: ' + (e === null));
    
    // Create safe event object
    const safeEvent = e || {};
    Logger.log('Safe event keys: ' + Object.keys(safeEvent).join(', '));
    
    let data = {};
    
    // Try to parse URL query parameters directly (for undefined event objects)
    // This is a workaround for Apps Script deployment issues
    try {
      const url = ScriptApp.getService().getUrl();
      Logger.log('Script URL: ' + url);
    } catch (urlError) {
      Logger.log('Could not get script URL: ' + urlError.toString());
    }
    
    // Try to get data from parameters (URL-encoded form data)
    if (safeEvent.parameter && Object.keys(safeEvent.parameter).length > 0) {
      Logger.log('Parsing URL-encoded data from safeEvent.parameter');
      Logger.log('Parameters: ' + JSON.stringify(safeEvent.parameter));
      data = {
        name: safeEvent.parameter.name || '',
        email: safeEvent.parameter.email || '',
        inquiryType: safeEvent.parameter.inquiryType || '',
        subject: safeEvent.parameter.subject || '',
        message: safeEvent.parameter.message || '',
        toolName: safeEvent.parameter.toolName || '',
        timestamp: safeEvent.parameter.timestamp || new Date().toISOString()
      };
    }
    // Try e.parameters (plural) - sometimes Apps Script uses this
    else if (safeEvent.parameters && Object.keys(safeEvent.parameters).length > 0) {
      Logger.log('Parsing URL-encoded data from safeEvent.parameters');
      Logger.log('Parameters: ' + JSON.stringify(safeEvent.parameters));
      data = {
        name: (safeEvent.parameters.name && safeEvent.parameters.name[0]) || '',
        email: (safeEvent.parameters.email && safeEvent.parameters.email[0]) || '',
        inquiryType: (safeEvent.parameters.inquiryType && safeEvent.parameters.inquiryType[0]) || '',
        subject: (safeEvent.parameters.subject && safeEvent.parameters.subject[0]) || '',
        message: (safeEvent.parameters.message && safeEvent.parameters.message[0]) || '',
        toolName: (safeEvent.parameters.toolName && safeEvent.parameters.toolName[0]) || '',
        timestamp: (safeEvent.parameters.timestamp && safeEvent.parameters.timestamp[0]) || new Date().toISOString()
      };
    }
    // Fallback to JSON parsing
    else if (safeEvent.postData && safeEvent.postData.contents) {
      Logger.log('Parsing JSON data from postData');
      Logger.log('Post data contents: ' + safeEvent.postData.contents);
      try {
        data = JSON.parse(safeEvent.postData.contents);
      } catch (parseError) {
        Logger.log('JSON parse error: ' + parseError.toString());
      }
    }
    else {
      Logger.log('No data found in parameter, parameters, or postData');
      Logger.log('Full event object: ' + JSON.stringify(safeEvent));
      
      // If we have no data at all, show the test/info page
      const html = `
        <html>
          <body>
            <h1>ShramTools Contact Form API</h1>
            <p>Status: ✅ Running</p>
            <p>This Web App is ready to receive contact form submissions.</p>
            <hr>
            <h2>Debug Info</h2>
            <p>Event object was empty. This page is shown when accessing the script URL directly.</p>
            <p>Form submissions should include URL parameters.</p>
            <hr>
            <p><a href="https://shramtools.shramkavach.com/contact.html">Go to Contact Form</a></p>
          </body>
        </html>
      `;
      return HtmlService.createHtmlOutput(html);
    }
    
    Logger.log('Parsed data: ' + JSON.stringify(data));
    
    // Validate required fields
    if (!data.name || !data.email || !data.subject || !data.message) {
      throw new Error('Missing required fields: ' + JSON.stringify({
        hasName: !!data.name,
        hasEmail: !!data.email,
        hasSubject: !!data.subject,
        hasMessage: !!data.message
      }));
    }
    
    // Get or create the spreadsheet sheet
    const sheet = getOrCreateSheet();
    Logger.log('Got sheet: ' + sheet.getName());
    
    // Add data to sheet
    addDataToSheet(sheet, data);
    Logger.log('Data added to sheet');
    
    // Send notification email to admin
    if (NOTIFICATION_EMAIL && NOTIFICATION_EMAIL !== 'your-email@example.com') {
      try {
        sendNotificationEmail(data);
        Logger.log('Notification email sent');
      } catch (emailError) {
        Logger.log('Email notification error: ' + emailError.toString());
      }
    }
    
    // Send auto-reply to user
    if (SEND_AUTO_REPLY && data.email) {
      try {
        sendAutoReply(data);
    const safeEvent = e || {};
    if (safeEvent.parameter) {
      Logger.log('Parameters: ' + JSON.stringify(safeEvent.parameter));
    }
    if (safeEvent.parameters) {
      Logger.log('Parameters (plural): ' + JSON.stringify(safeEvent.parameters));
    }
    if (safeEvent.postData) {
      Logger.log('Post data: ' + JSON.stringify(safeEventtringify({
      status: 'success',
      message: 'Form submitted successfully',
      data: data
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    // Log error with details
    Logger.log('ERROR: ' + error.toString());
    Logger.log('Stack: ' + error.stack);
    
    if (e && e.parameter) {
      Logger.log('Parameters: ' + JSON.stringify(e.parameter));
    }
    if (e && e.parameters) {
      Logger.log('Parameters (plural): ' + JSON.stringify(e.parameters));
    }
    if (e && e.postData) {
      Logger.log('Post data: ' + JSON.stringify(e.postData));
    }
    
    // Return error response
    return ContentService.createTextOutput(JSON.stringify({
      status: 'error',
      message: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
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
