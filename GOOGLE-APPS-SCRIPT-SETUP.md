# Google Apps Script Setup Guide for ShramTools Contact Form

## Overview
This guide will help you connect your contact form to Google Sheets using Google Apps Script to automatically save submissions and send email notifications.

## Step-by-Step Setup

### 1. Create a Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it "ShramTools Contact Form Submissions" (or any name you prefer)
4. Keep this tab open - you'll need it

### 2. Open Apps Script Editor

1. In your Google Sheet, click **Extensions** > **Apps Script**
2. This opens the Apps Script editor in a new tab
3. Delete any default code in the editor

### 3. Add the Script

1. Copy the entire content from `google-apps-script.js`
2. Paste it into the Apps Script editor
3. Customize the configuration section:
   ```javascript
   const SHEET_NAME = 'Submissions';  // Name of the sheet tab
   const NOTIFICATION_EMAIL = 'your-email@example.com';  // Your email
   const SEND_AUTO_REPLY = true;  // Set to false to disable auto-replies
   ```

### 4. Save the Script

1. Click the disk icon or press `Ctrl+S` (Windows) / `Cmd+S` (Mac)
2. Name your project: "ShramTools Contact Form Handler"
3. Click **Save**

### 5. Deploy as Web App

1. Click **Deploy** > **New deployment**
2. Click the gear/settings icon ⚙️ next to "Select type"
3. Choose **Web app**
4. Configure the deployment:
   - **Description**: "ShramTools Contact Form v1"
   - **Execute as**: "Me (your-email@gmail.com)"
   - **Who has access**: "Anyone"
5. Click **Deploy**

### 6. Authorize the Script

1. You'll see a warning "Authorization required"
2. Click **Authorize access**
3. Choose your Google account
4. Click **Advanced** (if you see a warning)
5. Click **Go to [Project Name] (unsafe)**
6. Click **Allow**

### 7. Copy the Web App URL

1. After authorization, you'll see a "Deployment" dialog
2. Copy the **Web app URL** - it looks like:
   ```
   https://script.google.com/macros/s/AKfycbx.../exec
   ```
3. **IMPORTANT**: Save this URL - you'll need it for the next step

### 8. Update Your Contact Form

1. Open `contact.html` in your code editor
2. Find this line (near the top of the `<script>` section):
   ```javascript
   const GOOGLE_SCRIPT_URL = 'YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL_HERE';
   ```
3. Replace `'YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL_HERE'` with your Web App URL:
   ```javascript
   const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbx.../exec';
   ```
4. Save the file

### 9. Test the Integration

1. **Test using the Web Interface:**
   - Visit your Web App URL in a browser
   - You should see a test page with a "Send Test Submission" button
   - Click the button to verify the setup
   - Check your Google Sheet for the test entry

2. **Test using the Apps Script function:**
   - In Apps Script editor, select `testSetup` from the function dropdown
   - Click the **Run** button (▶️)
   - Check your Google Sheet - you should see a test entry

3. **Test the live form:**
   - Open your `contact.html` page in a browser
   - Fill out and submit the form
   - Check your Google Sheet for the new submission
   - Check your email for the notification (if configured)

### 10. Important: Redeploy After Script Changes

**CRITICAL:** If you made any changes to the Apps Script code, you MUST create a new deployment:

1. In Apps Script editor, click **Deploy** > **New deployment**
2. Click the gear icon and select **Web app**
3. Change the version to "New version"
4. Add description: "ShramTools Contact Form v2" (or increment version)
5. Click **Deploy**
6. Copy the NEW Web App URL
7. Update the URL in `contact.html` if it changed

### 11. Deploy Your Updated Website

```bash
git add contact.html
git commit -m "Connect contact form to Google Apps Script"
git push
```

## Features

✅ **Automatic Data Storage**: All form submissions are saved to Google Sheets  
✅ **Email Notifications**: Get notified when someone submits the form  
✅ **Auto-Reply**: Users receive automatic confirmation emails  
✅ **Organized Data**: Submissions are neatly organized with timestamps  
✅ **Status Tracking**: Each submission has a status field you can update  

## Customization Options

### Change Email Templates

Edit the auto-reply template in the script:
```javascript
const AUTO_REPLY_SUBJECT = 'Your custom subject';
const AUTO_REPLY_BODY = `
Your custom email body with placeholders:
{name}, {email}, {subject}, {inquiryType}, {toolName}
`;
```

### Disable Email Notifications

Set these to `false` or `null`:
```javascript
const NOTIFICATION_EMAIL = null;  // Disable admin notifications
const SEND_AUTO_REPLY = false;    // Disable auto-replies
```

### Add More Fields

1. Update the form in `contact.html`
2. Add the field name to the data object in the script
3. Add a new column header in `getOrCreateSheet()` function
4. Add the value in `addDataToSheet()` function

## Troubleshooting

### Error: "Cannot read properties of undefined (reading 'postData')"

**Solution:** You need to create a NEW deployment after updating the script:
1. Go to Apps Script editor
2. Click **Deploy** > **New deployment**
3. Select **Web app**
4. Set version to "New version"
5. Click **Deploy**
6. Use the NEW URL in your contact.html

### Form Not Submitting
- Check browser console for errors (F12 > Console)
- Verify the Web App URL is correct in `contact.html`
- Make sure the deployment is set to "Anyone" access

### Not Receiving Emails
- Check spam folder
- Verify `NOTIFICATION_EMAIL` is set correctly
- Check Apps Script execution logs: Apps Script > Executions

### Data Not Appearing in Sheet
- Run `testSetup()` function to verify setup
- Check Apps Script execution logs for errors
- Verify sheet name matches `SHEET_NAME` constant

## Managing Submissions

### View Submissions
Open your Google Sheet to see all submissions in real-time

### Update Status
Change the "Status" column from "New" to:
- "In Progress"
- "Resolved"
- "Spam"
- Or any custom status

### Export Data
**File** > **Download** > Choose format (Excel, CSV, PDF)

## Security Notes

- The script runs under your Google account
- Only you can access the Google Sheet
- Form submissions are stored securely in Google Drive
- The Web App URL can be regenerated if needed

## Need Help?

- Check [Google Apps Script Documentation](https://developers.google.com/apps-script)
- Review execution logs in Apps Script editor
- Test with the `testSetup()` function

---

**Last Updated**: January 2026  
**Version**: 1.0
