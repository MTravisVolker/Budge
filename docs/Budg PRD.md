# Budgeting App PRD

## Product Overview

Budg is a web-based budgeting application designed to help users manage personal finances by tracking bank accounts, credit card accounts, and bills. It provides a clear view of current account balances, upcoming and paid bills, and projected balances after bill payments. Budget supports user-configurable categories and a user-selected date range for viewing financial data. It emphasizes manual data entry and excludes income tracking, notifications, or multi-currency support.

## Target Audience

- Individuals seeking a simple, clear tool to manage personal finances, including bills and account balances.
- Users who prefer manual control over their financial data without relying on invasive bank integrations or automated updates.

## Stakeholders
- Product Manager: Travis Volker
- Lead Developer: Travis Volker
- Web Frontend Designer: Travis Volker
- Database Administrator: Travis Volker
- Site Reliability Engineer: Travis Volker

## Why Build

While many budgeting apps exist, none offer Budg's simplicity and focus. Budg functions like a modern checkbook register, stripping away unnecessary features and optimizing for user-friendliness and essential functionality.

## Value Proposition

Discover the joy of effortless budgeting! Streamline your finances, stay on top of every payment, and keep your funds perfectly balanced. Feel a wave of satisfaction with every budgeting session, as our thoughtfully designed app delivers exactly the features you’ve always wanted. Experience the thrill of financial harmony and a sense of accomplishment like never before!

## Scope

### In-Scope
- **Budget Creation and Management**:
  - Recurrences
  - Due Bill Statuses
  - Bill Categories
  - Bank Accounts
  - Bills
  - Due Bills
  - Bank Account Instances
  - Audit Logs
- **User Authentication**:
  - Login
  - Signup
  - Password Reset
  - Multifactor Authentication
  - API Authentication Tokens
- **Automations**:
  - Automatically calculate the next Due Bill based on recurrence and the last Due Bill's due date.
- **Optimized and Modern UI**:
  - Simple, beautifully designed tables
  - Modal popups for data entry
  - Intuitive feature placement
  - Drag-and-drop table rows for prioritization

### Out-of-Scope
- **Mobile App**: Potential future development for mobile access.
- **Reporting**: Optional financial reports or summaries.
- **Automation**: Future bank API integration for automated balance updates.
- **User-Defined Recurrence Calculations**: Potential feature for custom recurrence logic.

## User Stories

### User Interface and Interaction

1. **As a Budg user**, I want a modern, intuitive web app design that is aesthetically pleasing.
2. **As a Budg user**, I want a responsive web app design that renders well and is easy to use on any device (PC, laptop, tablet, or mobile phone).

#### Due Bills and Bank Account Instance Management

3. **As a Budg user**, I want a clean, spreadsheet-like table view of my bills and accounts so that I can easily scan and understand my financial data.
4. **As a Budg user**, I want that spreadsheet-like table view to be the home page after I login so that I can instantly understand my financial data without having to click anything.
5. **As a Budg user**, I want to drag and drop bill rows to reorder them so that I can prioritize certain bills visually within the table.
6. **As a Budg user**, I want a value stored to a field called "priority" in the database when I drag and drop bill rows to reorder them so that they can render in the right order when the page is re-rendered.
7. **As a Budg user**, I want hover effects on table rows and columns to highlight the data I’m viewing so that I can focus on specific information without distraction.
8. **As a Budg user**, I want to use modal popups for adding or editing the following so that I can input data without navigating away from the main view:
   - Due Bills (used to track an instance/transaction of a bill)
   - Bank Accounts Instances (used to tack a balance of an instance of a bank account)
9. **As a Budg user**, I want inline controls (e.g., edit/delete icons) next to each bill and account so that I can quickly make changes without extra clicks.
10. **As a Budg user**, I want an edit modal popup when I double click a row in a table so that I can quickly edit the contents of the row.
11. **As a Budg user**, I want to be prompted to add my first bill if my bills list is blank so that I'm not confused when the page is blank.
12. **As a Budg user**, I want to add a new due bill with a name (foreign key reference to bill), recurrence (ForeignKey relationship to Recurrence), amount due, draft account (foreign key relationship to Account) defaulting to the draft account from the foreign key referenced bill, so that I can manage multiple bills in a modal from the home page.
13. **As a Budg user**, I want to add a new Bank Account Instance with a name (foreign key reference to Bank Accounts), balance, due date, pay date, status (ForeignKey relationship to Status), so that I can manage multiple Bank Account Instances in a modal from the home page.
14. **As a Budg user**, I want Bank Account Instance and Due Bill rows to be highlighted the color of their status (Foreign Key Status highlight color) so that the status of a row is obvious at a glance.
15. **As a Budg user**, I want all text in the row for Bank Account Instance to have the font color from foreign key reference font color in bank account.
16. **As a Budg user**, I don't want the table to be rendered if my bills list is blank so that the interface is clean and accurate.
17. **As a Budg user**, I want to select a custom date range for viewing my bills so that I can focus on a specific period, such as the current month or quarter.
18. **As a Budg user**, I want the custom date range selector start date to default to two weeks before my next account balance.
19. **As a Budg user**, I want the custom date range selector end date to default to four weeks after my next account balance.
20. **As a Budg user**, I want to see a list of all paid and upcoming bills within my selected date range, grouped by bank account/draft account, so that I can understand my financial commitments at a glance.
21. **As a Budg user**, I want to view the projected balance for each bank account after upcoming bills are paid so that I can plan my spending and avoid overdrafts. I envision this as subtotals at the end of each group of bank accounts/draft accounts.
22. **As a Budg user**, I want the bill list to be ordered by draft account, priority, pay date, then due date, so that I can prioritize payments based on what’s due soonest.
23. **As a Budg user**, I want a list of nested tabs above the table view so that I can access all of the management pages.
24. **As a Budg user**, I want drop-down selectors to include an add at the bottom which will bring me to an add modal so that I can add a new of whatever the drop-down selector was selecting.
25. **As a Budg user**, I want "Add" hyperlinks next to each label for a drop-down selector so that I can add one of whatever is listed in the drop-down selector without having to open the drop-down selector.
26. **As a Budg user**, I want individual pages to list out and manage each of the following: 
    - Due Bill Statuses
    - Recurrences
    - Bank Accounts
    - Bills
27. **As a Budg user**, I don't want individual pages to list out and manage each of the following because they'll be managed from the home page table view.              
    - Bank Account Instances
    - Due Bills
28. **As a Budg user**, I want to manually enter the current balance for my Bank Account Instance so that I can see an accurate starting point for my financial overview.

#### Account Management

29. **As a Budg user**, I want to add a new bank with a name, and font color so that I can manage multiple accounts in one place.
30. **As a Budg user**, I want to edit or delete an existing bank so that I can keep my account list up-to-date if my financial accounts change.

#### Bill Management

31. **As a Budg user**, I want to add a new bill with a name, default amount due, url, draft account (foreign key relationship to Account), category, recurrence so that I can manage multiple bills in one place.
32. **As a Budg user**, I want to edit or delete an existing bill so that I can keep my bill list up-to-date if my financial accounts change.
33. **As a Budg user**, I want to set a bill as with a particular recurrence (monthly, bi-monthly, n number of days, n number of months or anually) so that I don’t have to manually enter it for each occurrence.
34. **As a Budg user**, I want Budg to automatically generate the next due date for a recurring Due Bill based on its recurrence pattern so that I can see upcoming bills without manual entry.

#### Recurrence Management

35. **As a Budg user**, I want to add a new recurrence with a name, and calculation so that I can manage multiple recurrences in one place.
36. **As a Budg user**, I want to to edit or delete an existing recurrence so that I can keep my recurrence list up-to-date if my financial accounts change.
   
#### Due Bill and Bank Account Instance Status Management

37. **As a Budg user**, I want to add a new status with a name, and highlight color so that I can manage multiple statuses in one place.
38. **As a Budg user**, I want to to edit or delete an existing statuses so that I can keep my status list up-to-date if my financial accounts change.
39.   

#### Category Management

40. **As a Budg user**, I want to create custom categories for my bills (e.g., Utilities, Food, Date, Bad Debt, Good Debt, Insurance) so that I can organize my expenses in a way that makes sense to me.
41. **As a Budg user**, I want to edit or delete existing categories so that I can refine my categorization system as my needs evolve.
42. **As a Budg user**, I want to assign a category to each bill when creating or editing it so that I can group similar expenses together for clarity.

### Authentication and Security

43. **As a Budg user**, I want to sign up for an account with a secure login so that my financial data is protected and accessible only to me.
44. **As a Budg user**, I want to log in to Budg securely so that I can access my financial data from any modern web browser.
45. **As a Budg user**, I want to reset my password if I forget it so that I can regain access to my account without losing my data.
46. **As a Budg user**, I want to enable multifactor authentication so that I can add an extra layer of security to my account.

### Automation

47. **As a Budg user**, I want to prompt Budg to create new Due Bills and Bank Account Instances by calculating due dates and payment dates from previous due dates and payments dates along with the recurrence setting so that I don't have to manually create these enteries after I create them the first time.

## User Interface

### Primary List View

- **Spreadsheet Looking Modern Html Table**: The list will be a simple tableview.
- **Row and Column Hightlights**: The table will have alternating row colors. And the row will and column will darken when the mouse hovers over it.
- **Date Range Selector**: Users set a start and end date to filter bills. A React.js date range selector tool will be used.
- **Default Value for Date Range Selector**: 
- **Grouped by Bank Account**: Each section displays the account name and current balance.
- **Bills Ordered by Due Date**: Lists all bills (paid and upcoming) within the date range.
- **Projected Balances**: For upcoming bills, show the balance after each bill.
- **Bill Status**: Indicate whether each bill is "Paid" or "Upcoming."
- **CRUD Controls**: Inline options to add, edit, or delete bills and accounts.

**Example Layout:**


### Additional Pages

- **Bank Account Management**: View and update bank account details.
- **Bill Management**: View and update bill details.
- **Category Management**: Interface for users to manage categories.
- **Status Management**: Interface for users to manage statuses.
- **Recurrence Management**: Interface for users to manage recurrences.

## Technical Considerations

- **Manual Data Entry**: No bank integrations; users are responsible for updating balances and bill statuses.
- **Single Currency**: All amounts are treated as being in one currency.
- **Data Security**: Financial data is stored securely with encryption.
- **User Authentication**: Secure login and registration to protect user data.

## Non-Functional Requirements

- **Usability**: The app should be intuitive for users with basic financial knowledge.
- **Performance**: The app should load quickly, even with a large number of bills and accounts.
- **Scalability**: The app should support multiple users with their own data sets.

## Assumptions and Constraints

- **Assumptions**:
  - Users will manually enter and update their financial data.
  - The app does not need to handle multiple currencies.
  - Notifications are not required.

- **Constraints**:
  - No automated data fetching from banks or financial institutions.
  - The app must be web-based and accessible via modern browsers.

## Success Metrics

- **User Satisfaction**: High user satisfaction with the clarity and usability of the financial overview.
- **Adoption**: A growing number of users actively managing their bills and accounts.
- **Retention**: Users continue to use the app over time to manage their finances.