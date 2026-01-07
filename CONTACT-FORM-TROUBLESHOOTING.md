# Contact Form Troubleshooting Guide

## Form Not Updating Google Sheet? Follow These Steps:

### ✅ Step 1: Update the Apps Script Code

1. Open your Google Sheet
2. Go to **Extensions** > **Apps Script**
3. **Replace ALL code** with the updated code from `google-apps-script.js`
4. **Save** (Ctrl/Cmd + S)

### ✅ Step 2: Create a NEW Deployment (CRITICAL!)

**This is the most common issue - you MUST create a new deployment after changing the code!**

1. In Apps Script, click **Deploy** > **New deployment**
2. Click the gear icon ⚙️ next to "Select type"
3. Select **Web app**
4. Set:
   - Description: "Contact Form v3" (or increment your version)
   - Execute as: **Me**
   - Who has access: **Anyone**
5. Click **Deploy**
6. **Authorize** if prompted
7. **Copy the new Web App URL**

### ✅ Step 3: Update the URL in contact.html

1. Open `contact.html`
2. Find this line (around line 497):
   ```javascript
   const GOOGLE_SCRIPT_URL = 'YOUR_OLD_URL';
   ```
3. Replace with your NEW URL from Step 2
4. Save the file

### ✅ Step 4: Test Directly in Apps Script

1. In Apps Script editor, select `testSetup` from the dropdown
2. Click **Run** (▶️)
3. Check your Google Sheet - you should see a test entry
4. If this works, the script is configured correctly

### ✅ Step 5: Test the Live Form

1. Open `contact.html` in your browser (use the live URL, not local file)
2. Fill out the form completely
3. Click Submit
4. Open **Browser Console** (F12 > Console tab)
5. Look for any error messages
6. Check your Google Sheet for the new entry

### ✅ Step 6: Check Apps Script Logs

1. In Apps Script editor, click **Executions** (left sidebar, clock icon)
2. Look for recent executions
3. Click on any execution to see logs
4. Look for errors or check what data was received

## Common Issues & Solutions

### Issue: "Form submitted" message shows but no data in sheet

**Solution:** You're using an OLD deployment URL. Create a NEW deployment (Step 2 above).

### Issue: Console shows "Failed to fetch" or network error

**Possible causes:**
- Wrong URL in contact.html
- Deployment not set to "Anyone" access
- Script not authorized

**Solution:**
1. Verify URL is correct
2. Redeploy with "Anyone" access
3. Reauthorize the script

### Issue: Data appears in sheet but no emails sent

**Solution:** 
1. Check `NOTIFICATION_EMAIL` in the script (must not be 'your-email@example.com')
2. Check spam folder
3. Look at Apps Script execution logs for email errors

### Issue: Form shows error message immediately

**Cause:** Missing required fields or JavaScript error

**Solution:**
1. Check browser console for errors
2. Verify all required fields have values
3. Check that form field names match script expectations

## Debugging Steps

### 1. Check Browser Console
```
F12 > Console tab
Look for:
- "Submitting form data:" (should show your data)
- "Response received:" (should appear after submission)
- Any red error messages
```

### 2. Check Apps Script Logs
```
Apps Script > Executions (left sidebar)
Recent execution > View logs
Look for:
- "Received POST request"
- "Parsing URL-encoded data" or "Parsing JSON data"
- "Parsed data: {...}"
- "Data added to sheet"
```

### 3. Test with Simple Data
Fill the form with basic test data:
- Name: Test User
- Email: test@test.com
- Inquiry Type: General Question
- Subject: Test
- Message: This is a test
- Submit and check sheet

## Quick Verification Checklist

- [ ] Updated script code in Apps Script editor
- [ ] Saved the script
- [ ] Created NEW deployment (not reused old one)
- [ ] Copied NEW Web App URL
- [ ] Updated URL in contact.html
- [ ] Deployment set to "Anyone" access
- [ ] Script authorized when prompted
- [ ] testSetup() function works
- [ ] Checked browser console for errors
- [ ] Checked Apps Script execution logs

## Still Not Working?

1. **Delete the old deployment:**
   - Apps Script > Deploy > Manage deployments
   - Click archive icon on old deployments
   - Create fresh new deployment

2. **Start from scratch:**
   - Create new Google Sheet
   - Follow GOOGLE-APPS-SCRIPT-SETUP.md from step 1

3. **Verify the sheet:**
   - Make sure sheet is named "Submissions" or update SHEET_NAME in script
   - Check if headers exist in row 1

## Contact Form Data Flow

```
User fills form
    ↓
JavaScript collects data
    ↓
fetch() sends to Google Apps Script URL
    ↓
doPost(e) receives data
    ↓
Data parsed and validated
    ↓
Added to Google Sheet
    ↓
Emails sent (if configured)
    ↓
Success response returned
```

## Need More Help?

Check these resources:
1. Apps Script execution logs (most helpful!)
2. Browser console errors
3. Google Apps Script documentation
4. Check that web app is public ("Anyone" access)

---

**Last Updated:** January 2026
