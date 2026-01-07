/**
 * ShramTools Contact Form - Google Apps Script
 * Simple, working version - Start fresh!
 */

// Configuration
var SHEET_NAME = 'Submissions';
var NOTIFICATION_EMAIL = 'shramkavach@gmail.com';

// Handle POST requests
function doPost(e) {
  return handleFormSubmission(e);
}

// Handle GET requests  
function doGet(e) {
  return handleFormSubmission(e);
}

// Main handler
function handleFormSubmission(e) {
  try {
    // Get form data
    var params = e.parameter;
    
    // Validate
    if (!params.name || !params.email || !params.subject || !params.message) {
      return createResponse('error', 'Missing required fields');
    }
    
    // Save to sheet
    var sheet = getSheet();
    sheet.appendRow([
      new Date(),
      params.name,
      params.email,
      params.inquiryType || '',
      params.subject,
      params.message,
      params.toolName || '',
      'New'
    ]);
    
    // Send email notification
    sendEmail(params);
    
    // Success response
    return createResponse('success', 'Form submitted successfully');
    
  } catch (error) {
    Logger.log('Error: ' + error.toString());
    return createResponse('error', error.toString());
  }
}

// Get or create sheet
function getSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow(['Timestamp', 'Name', 'Email', 'Inquiry Type', 'Subject', 'Message', 'Tool Name', 'Status']);
    sheet.getRange(1, 1, 1, 8).setFontWeight('bold').setBackground('#667eea').setFontColor('#ffffff');
  }
  
  return sheet;
}

// Send notification email
function sendEmail(data) {
  try {
    MailApp.sendEmail({
      to: NOTIFICATION_EMAIL,
      subject: 'New Contact: ' + data.inquiryType,
      body: 'Name: ' + data.name + '\nEmail: ' + data.email + '\nType: ' + data.inquiryType + '\nSubject: ' + data.subject + '\nMessage: ' + data.message + '\nTool: ' + (data.toolName || 'N/A')
    });
  } catch (e) {
    Logger.log('Email error: ' + e.toString());
  }
}

// Create JSON response
function createResponse(status, message) {
  var output = JSON.stringify({status: status, message: message});
  return ContentService.createTextOutput(output).setMimeType(ContentService.MimeType.JSON);
}
