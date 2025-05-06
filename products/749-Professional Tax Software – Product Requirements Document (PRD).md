# Professional Tax Software – Product Requirements Document (PRD)

## Table of Contents

- **1. Introduction**

  - 1.1 Purpose and Scope
  - 1.2 Product Overview
  - 1.3 Target Users and Audience
  - 1.4 Goals and Objectives
  - 1.5 Out of Scope

- **2. Professional vs. Corporate Tax Software**

  - 2.1 Distinct Use Cases and Users
  - 2.2 Key Differences in Features

- **3. User Roles and Permissions**

  - 3.1 Tax Preparer (Primary User)
  - 3.2 Reviewer/Manager (Secondary User)
  - 3.3 Firm Administrator
  - 3.4 Client (Taxpayer) – External Portal User
  - 3.5 Role-Based Access Control Matrix

- **4. Workflow Overview and Data Lifecycle**

  - 4.1 Client Onboarding and Data Collection
  - 4.2 Tax Return Preparation Process
  - 4.3 Review and Quality Assurance
  - 4.4 Client Review and Approval (E-Signature)
  - 4.5 Filing (Submission to Tax Agencies)
  - 4.6 Post-Filing, Support, and Record Keeping

- **5. Client Information Management**

  - 5.1 Client Profile Database
  - 5.2 Contact and Identity Information (Tax IDs, Filing Status, etc.)
  - 5.3 Client Document Management
  - 5.4 Managing Deadlines and Tasks per Client

- **6. Tax Return Preparation & Computation**

  - 6.1 Support for Individual Tax Returns (1040 series)
  - 6.2 Support for Business Tax Returns (1120, 1120S, 1065, etc.)
  - 6.3 Tax Calculation Engine (Automated Calculations)
  - 6.4 Compliance Rules and Error Checking
  - 6.5 Handling Tax Law Updates

- **7. Tax Forms Coverage (Federal, State, Local)**

  - 7.1 Supported Federal Forms and Schedules
  - 7.2 Supported State and Local Tax Forms
  - 7.3 Annual Updates to Forms and Rates
  - 7.4 Extension and Amended Return Support

- **8. Electronic Filing (E-Filing) Process**

  - 8.1 E-File Preparation (Data Packaging in IRS format)
  - 8.2 Transmission to IRS and State Systems
  - 8.3 Acknowledgment Handling (Accepted/Rejected)
  - 8.4 Error Resolution and Resubmission
  - 8.5 E-File Status Tracking and Notifications
  - 8.6 IRS and State E-File Compliance (ATS Certification)

- **9. Data Import and Integration**

  - 9.1 Import from Accounting Platforms (e.g. QuickBooks)
  - 9.2 Import of Prior Year Returns and Data
  - 9.3 Third-Party Data Sources (Payroll, Financial Institutions)
  - 9.4 APIs and Data Exchange Mechanisms

- **10. E-Signature Functionality**

  - 10.1 Integrated E-Signature Workflow
  - 10.2 Compliance with IRS E-Sign Regulations
  - 10.3 Client Authentication and Audit Trail for Signatures
  - 10.4 Document Storage and Retrieval

- **11. Tax Planning and Reporting**

  - 11.1 Tax Planning Tools (What-If Scenarios, Projections)
  - 11.2 Historical Data Analysis and Year-over-Year Comparison
  - 11.3 Client Tax Reports and Summaries
  - 11.4 Firm-Level Reports (Productivity, Revenue, etc.)

- **12. Payment and Fee Handling**

  - 12.1 Invoicing and Direct Payment Collection
  - 12.2 Fee Deduction from Tax Refund (Integration with Bank Products)
  - 12.3 Refund Distribution and Tracking
  - 12.4 Payment Processing Security and Compliance

- **13. Audit Trail and Logging**

  - 13.1 Change Tracking (Who, What, When)
  - 13.2 Access Logs and Activity Monitoring
  - 13.3 Audit Trail for Compliance and Reviews
  - 13.4 Reporting and Export of Audit Logs

- **14. Integration with External Systems**

  - 14.1 Accounting Software Integration
  - 14.2 Banking and Payment Gateways
  - 14.3 Third-Party Services (e.g. Payroll, Document Management)
  - 14.4 Open API for Custom Integrations

- **15. Deployment and Hosting Options**

  - 15.1 Cloud (SaaS) Deployment
  - 15.2 On-Premise Deployment
  - 15.3 Hybrid Considerations
  - 15.4 Multi-Tenancy and Data Isolation

- **16. Non-Functional Requirements**

  - 16.1 Performance and Scalability
  - 16.2 Security and Data Privacy
  - 16.3 Regulatory Compliance
  - 16.4 Availability and Reliability
  - 16.5 Maintainability and Supportability

- **17. Appendix**

  - 17.1 Glossary of Terms
  - 17.2 References

---

## 1. Introduction

### 1.1 Purpose and Scope

This Product Requirements Document (PRD) outlines the features, functionalities, and constraints for a **Professional Tax Software** application. The document is intended for product managers at a SaaS company who will guide the development of a comprehensive tax preparation platform for professional use. It covers all aspects of the system – from functional capabilities (client management, tax filing, compliance features, integrations, etc.) to non-functional requirements (performance, security, scalability, compliance standards, etc.). The scope includes requirements for both **cloud-based (SaaS)** and **on-premise** deployments of the software.

The primary focus of this software is on **professional tax preparation** – i.e., a tool used by tax professionals (such as tax preparers, Certified Public Accountants (CPAs), and Enrolled Agents) to manage multiple clients and prepare/file taxes on their behalf. This is distinct from consumer tax software for individuals or enterprise “corporate” tax solutions, as detailed below. The system is expected to support preparation of **individual and business tax returns**, ensure compliance with relevant tax laws, facilitate electronic filing, and streamline the end-to-end workflow of a tax preparer’s office.

All requirements in this document are intended to ensure that the resulting product meets the needs of a busy tax practice: managing client information securely, preparing accurate tax returns efficiently, collaborating with clients for approvals, and staying compliant with regulatory standards. Both functional requirements (what the system should do) and non-functional requirements (performance, security, etc.) are specified to provide a complete picture of the product expectations.

### 1.2 Product Overview

The Professional Tax Software is a **comprehensive tax preparation and filing system** for professional use. It will serve as a one-stop platform for tax firms to handle all aspects of their clients’ tax needs. Key capabilities of the system (at a high level) include:

- **Client Information Management:** Maintain a database of clients with their personal/business details, tax identification numbers, prior year data, filing status, etc.. This functions as a mini-CRM tailored to tax preparers.
- **Tax Return Preparation:** Calculate and prepare tax returns for **individuals (Form 1040 and variants)** and **business entities** (e.g., partnerships, S-corps, C-corps, etc.), with an engine that ensures calculations are accurate and compliant with current tax laws. The software will produce all required forms and schedules for federal, state, and local filings.
- **Electronic Filing (E-Filing):** Transmit completed returns electronically to the IRS and state tax authorities. The system will handle e-filing submissions, track acknowledgments (acceptances/rejections), and manage errors or re-submissions as needed, providing a fully compliant e-file process.
- **Deadline and Compliance Management:** Ensure adherence to tax deadlines (e.g., filing deadlines, extension deadlines) by providing reminders, status tracking (e.g., which clients are due for filing), and the ability to file extensions. The system enforces tax law constraints and performs error-checking and validation to catch issues before filing.
- **Data Import and Integration:** Import relevant financial data from external sources – for example, integrating with accounting software (like QuickBooks or Xero) to pull in financials for business returns, importing prior year returns or client data (from last year’s files or IRS transcripts), and capturing data from third-party sources (such as 1099 forms from financial institutions).
- **Tax Forms Coverage (Federal, State, Local):** Support a wide range of tax forms across federal, all state jurisdictions, and common local jurisdictions. This includes individual income tax forms, corporate and business tax forms, estate/trust returns, nonprofit returns, and associated schedules. Having comprehensive form coverage ensures the professional can handle any client scenario.
- **Built-in E-Signature for Client Approvals:** Provide an integrated electronic signature solution so clients can review and sign tax documents (for example, signing Form 8879 IRS e-file authorization) digitally. This eliminates the need for physical signatures and speeds up the approval process by allowing remote authorization.
- **Tax Planning and Reporting:** Use current and historical data to assist in tax planning. The system will offer tools to project future tax situations or model “what-if” scenarios, and generate reports (for example, a comparison of this year vs. last year’s taxes, or a report on estimated quarterly taxes) to provide value-added advisory services.
- **Payment Handling and Fee Collection:** Facilitate the collection of service fees from clients. This includes options to invoice and collect payments directly, as well as the ability to deduct preparer fees from client tax refunds (in partnership with banking services) so that the preparer can get paid out of the refund if the client prefers. The software should also handle directing tax refunds to clients or processing any tax payments due.

These capabilities align with the standard definition of professional tax preparation software. As noted in industry analyses, professional tax software is designed to **streamline the tax prep process with high accuracy and compliance**, can be offered via cloud or on-premise deployments, and often integrates with accounting systems for data import. In essence, this product will provide “everything needed to succeed and grow a tax preparation business,” similar to other products in this space.

### 1.3 Target Users and Audience

The target users for this software are **tax professionals** who prepare returns on behalf of clients. This includes:

- **Tax Preparers and Accountants:** Individuals or teams in tax preparation firms, CPA firms, or independent tax businesses who file taxes for many clients. These users need efficiency, accuracy, and the ability to handle a high volume of returns during tax season.
- **Certified Public Accountants (CPAs) and Enrolled Agents (EAs):** Licensed professionals who require robust software to manage complex tax situations across multiple clients.
- **Tax Preparation Firms and Enterprises:** The application should scale from a solo practitioner up to mid-sized firms where multiple preparers and reviewers work collaboratively. (Note: By “enterprises” here we mean larger tax prep companies, not non-tax corporates—see Section 2 for distinction.)
- **Firm Administrators:** Individuals managing the operations of a tax firm, who might not prepare returns themselves but oversee staff, configure software settings, manage billing and see high-level status of all clients.
- **Clients (Taxpayers):** While not primary users of the software’s back-end, clients interact through features like reviewing their returns and electronically signing documents. They may access a client portal to upload documents or review tax summaries as part of the workflow.

Importantly, **the software is not aimed at corporate in-house tax departments** or end-consumers doing their own taxes. It’s designed for those who **“prepare and file tax returns for individuals and businesses”** as a service. The needs of these professional users drive the requirements: multi-client management, multi-user collaboration, high levels of compliance checks, support for many form types, and integration with practice workflows (e.g., client communication and signatures).

### 1.4 Goals and Objectives

The overarching goal is to provide a **complete professional tax SaaS solution** that increases the productivity of tax preparers while ensuring accuracy and compliance. Key objectives include:

- **Efficiency and Automation:** Automate repetitive and complex calculations, form filling, and data transfers. By **adopting a digital tax workflow with automation, cloud accessibility, integrated e-filing, and e-signatures, firms can streamline the entire process, improving productivity and turnaround time**. This means preparers spend less time on manual data entry and more on advising clients.
- **Accuracy and Compliance:** Incorporate robust validation engines and up-to-date tax law rules so that returns are calculated correctly and meet IRS/state regulations. The software should **provide error-checking and catch compliance issues** (e.g., missing information, contradictory inputs) before filing, reducing rejections and audits.
- **Comprehensive Coverage:** Support the breadth of scenarios a tax professional may encounter – from a simple individual return to a complex multi-state business return. This includes having all the necessary forms and supporting schedules, handling state/local variations, and even support for less common entities (trusts, exempt organizations) so that preparers rarely have to say “my software can’t do that.”
- **User Experience and Collaboration:** Offer a user-friendly interface that can be easily navigated by preparers (especially during the hectic tax season when speed matters). Support multi-user collaboration (multiple staff working on the same client or return) with proper controls. Provide tools to organize and manage workflow (status tracking, assignments, checklists) which is crucial when handling hundreds or thousands of returns.
- **Client Service and Transparency:** Provide features that enhance the interaction with clients – e.g., a secure client portal for document exchange and review, the ability to generate client-friendly reports or summaries, and easy electronic signature collection. These features make the tax preparation process smoother for clients and give the firm a professional, modern edge.
- **Security and Trust:** Given the sensitive nature of tax data, a paramount objective is to ensure data security and privacy at every step. The system must inspire confidence that client data is safe through strong encryption, access controls, audit trails, and compliance with data protection regulations. (Clients and professionals should feel their information is as secure as it would be in a bank’s system.)
- **Regulatory Compliance:** The product should meet or exceed all requirements set by tax authorities for software that files returns. For example, to be an IRS-approved software for e-filing, it must pass the IRS’s **Modernized e-File (MeF) Assurance Testing System (ATS)** each year. It should comply with IRS e-file provider rules (such as those in IRS Publication 1345 regarding e-signatures, etc.) and any state-specific electronic filing regulations.
- **Scalability and Availability:** The system should reliably handle peak tax season loads and be available whenever users need it, especially around major deadlines. In the cloud deployment, this means designing for high uptime and the ability to scale resources for heavy usage periods. For on-premise, it means the software is optimized and can be deployed in a robust configuration by the user’s IT team.
- **Flexibility (Deployment and Integration):** Offer deployment flexibility (cloud vs on-prem) to accommodate different firm policies. Also, integrate well with other tools and systems a firm uses – not just accounting software, but possibly document management systems, calendars/task management, etc., through APIs or built-in integrations. The software should fit into the broader ecosystem of a tax practice without requiring disruptive changes to everything else.

These objectives ensure the product not only meets functional needs but also delivers business value by improving how tax professionals work and serve their clients. The end result should be a **competitive professional tax software solution** that stands out in terms of features, compliance, and ease of use, helping firms “thrive in a competitive, digital-first marketplace”.

### 1.5 Out of Scope

To clarify, the following are outside the scope of this product:

- **Corporate Tax Provisions and Large-Enterprise Tax Management:** The software is not intended to handle complex corporate tax accounting for Fortune 500 companies (e.g., global tax consolidations, advanced tax provisioning for financial statements, etc.). Those needs are typically met by specialized corporate tax solutions. Our focus is on **tax preparers serving external clients**, not internal corporate tax departments.
- **DIY Consumer Tax Preparation:** This is not a consumer-oriented tax prep website for individuals to file their own taxes. While the professional may use the software to assist individuals, every return in the system is assumed to be prepared or overseen by a tax professional (not self-service by laypersons).
- **Accounting/Bookkeeping General Ledger Functions:** The software will import financial data but will not serve as a full accounting system or bookkeeping tool. It won’t have general ledger, accounts payable, etc. Those functions remain in external accounting software (with which we integrate). Only tax-specific accounting (like depreciation schedules, carryover calculations) are in scope.
- **Non-Tax Compliance Filings:** Other filings like payroll tax filings, sales tax returns, or company annual reports are not the primary focus (unless they are inherently part of a business’s income tax return process). The software may integrate or provide add-ons for those, but core requirements center on income tax returns (federal, state, local).
- **Legal or Tax Research Content:** The product is not a tax research platform (though integration with one could be considered a future enhancement). It won’t contain an entire tax law library or research citations within the preparation interface, beyond basic help for form fields. Tax professionals will use separate research tools as needed.
- **Practice Management Functions Beyond Tax Workflow:** While we include workflow and status tracking for returns, a full practice management suite (scheduling appointments, CRM beyond client tax info, employee time tracking, billing/invoicing outside of tax prep fees, etc.) is mostly out of scope except where directly related to completing tax returns. The focus is the tax prep and filing process itself.

By delineating the scope, we ensure that the requirements stay focused on building the best tax preparation software for professionals, without venturing into areas that would dilute the effort or require entirely different expertise.

---

## 2. Professional vs. Corporate Tax Software

Professional tax software should not be confused with corporate tax software – they serve different purposes and audiences. This section highlights the distinctions to clarify the intended use of our system and ensure we meet the specific needs of professional tax preparers.

### 2.1 Distinct Use Cases and Users

- **Professional Tax Software (Our Focus):** Built for tax preparers, accounting firms, and tax service businesses that handle tax filings for **multiple clients** (individuals or small/medium businesses). Users of professional tax software are service providers – they prepare returns for others. For example, a CPA may use this software to file 500 individual tax returns for various clients in a season. The software supports managing many client profiles and returns concurrently. Key users include CPAs, EAs, tax preparers, and their support staff.

- **Corporate Tax Software:** Used by **large companies or corporations** to manage their own internal tax obligations. The users are typically in-house corporate tax departments preparing the company’s taxes (e.g., a multinational corporation’s income tax, sales tax, VAT, etc.). This software often deals with consolidation of large financial data, complex provision calculations for accounting, and compliance needs for a single entity (or a corporate group). The “client” is the company itself. Users are corporate tax professionals within one organization.

**Key Use Case Difference:** Professional tax software is about one-to-many (one firm managing many taxpayers’ filings), whereas corporate tax software is one-to-one (one company managing its own taxes, which might be complex but are still for that single entity). Our product is firmly in the one-to-many camp, optimizing for multi-client management.

### 2.2 Key Differences in Features

Because of the different use cases, the feature sets have some overlap but several differences in emphasis:

- **Multi-Client Management:** Professional software emphasizes client management (storing separate profiles for each taxpayer, organizing by household or business, etc.). Corporate software typically does not need multi-client features – it might handle subsidiaries, but that’s within one corporate group rather than unrelated clients.

- **Forms Supported:** Professional software needs a broad range of forms (1040, 1120, 1120S, 1065, 1041, 990, etc., plus all state equivalents) to serve any client that walks in. Corporate software might focus on specific forms like the corporate income tax return (e.g., 1120 for the U.S.) and related international forms, but not individual 1040s or unrelated business forms.

- **Complexity of Tax Calculation:** Corporate tax solutions often have specialized capabilities for things like tax provision (deferred taxes for GAAP reporting), handling huge asset depreciation schedules, or multi-state apportionment for large corporations. Professional tax software, while robust, is tuned to handle common small business complexity and individual scenarios; it might not handle, say, multi-country tax treaties or advanced consolidation out of the box, which corporate software might.

- **User Roles:** In professional software, roles revolve around preparers, reviewers, and firm admins across many clients. In corporate software, roles might be by function (tax accounting, compliance officer, etc.) within one corporation’s data.

- **Integration Focus:** Professional software integrates with accounting packages that small businesses use (to pull in data), e-signature for clients, and bank products for fee collection. Corporate software integrates with ERPs (like SAP or Oracle) to gather financial data, and with financial reporting systems. Our integration needs (Section 14) will highlight things like QuickBooks integration rather than SAP, aligning with small business contexts.

- **Compliance and Updates:** Both types must keep up with laws, but professional software updates a wide array of tax law changes annually (for individual and various business taxes), whereas corporate might focus on changes affecting corporate taxation. Professional software must also comply with IRS e-filing standards for each form type and support preparer-specific compliance (e.g., IRS PTINs, e-file signature forms, etc.).

In summary, **“corporations and enterprises use corporate tax software to handle complex taxation, whereas tax professionals and firms who prepare and file tax returns for individuals and businesses use professional tax software”.** Our product firmly falls into the latter category. We will ensure features like multi-client handling, broad form support, e-signatures, and fee deduction options are front-and-center – features that would be irrelevant in a pure corporate context but are essential for professional preparers. Conversely, large-scale corporate-specific features (like global tax provision calculation) are not in scope, as noted.

This distinction is critical for positioning the product and making design decisions that best serve our intended users.

---

## 3. User Roles and Permissions

The system will be used by various types of users within a tax preparation firm, as well as by clients in a limited capacity. Defining user roles and their permissions is crucial for both security and workflow purposes. Below are the primary user roles in the system:

### 3.1 Tax Preparer (Primary User)

**Description:** The Tax Preparer is the typical end-user – a professional who prepares tax returns for clients. This could be a CPA, an enrolled agent, or an unlicensed tax preparer in a tax office.

**Key Responsibilities and Tasks:**

- Create new client records and input/update client information (personal details, dependent info, prior year carryovers, etc.).
- Input financial and tax data into the system for each client (enter W-2s, 1099s, income, deductions, etc. into the tax forms or worksheets).
- Use the tax calculation engine to compute tax liabilities and refunds.
- Review automatically generated alerts or errors (e.g., missing data or inconsistent entries) and correct data as needed.
- Generate draft tax returns and reports to review internally or with a senior preparer.
- Prepare final tax return forms for client and ensure everything is ready for filing.
- Initiate the e-signature request to the client for required forms (like e-file authorization).
- Submit e-filings to IRS/state once approved, or prepare printed returns if e-filing is not possible.
- Communicate with clients via notes or the client portal regarding additional information needed.
- Address e-file rejections by reviewing error messages and fixing return data accordingly.

**Permissions:**

- **Read/Write Access** to all tax data for clients they handle (they may have either access to only their assigned clients or all clients, depending on firm policy – the system should allow filtering by assignment).
- Can create new returns and edit returns in progress.
- Can generate and view any forms and reports for their clients.
- Can initiate (but maybe not finalize) e-filing – some firms might require a second person to review or a firm admin to actually transmit.
- Can send documents for e-signature to their clients.
- Cannot manage global settings or user accounts (limited to the data and functions of return preparation).
- If a preparer is designated as a **Reviewer** as well (small firms might have preparers review each other’s work), they might have permission to mark returns as reviewed or add review comments.

### 3.2 Reviewer/Manager (Secondary User)

**Description:** In some firms, a more senior accountant or a quality control manager acts as a **Reviewer** for returns prepared by others. This could be a role assigned to a senior CPA who reviews all returns for accuracy and compliance before they are finalized. In other cases, this role could be combined with Firm Admin or be just an experienced preparer.

**Key Responsibilities:**

- Review completed tax returns prepared by others for accuracy, completeness, and adherence to tax laws.
- Use the software’s review tools (like diagnostics, comparison against prior year, anomaly detectors) to identify any issues.
- Provide feedback or corrections to the preparer (possibly entering review notes in the system).
- Approve the return for filing once satisfied (the system might have a status change like “Reviewed/Approved”).
- Ensure proper documentation (workpapers, client docs) are attached in the system for audit trail.
- Possibly handle more complex clients directly as a preparer as well (overlap with preparer role).

**Permissions:**

- Read access to all returns (or all returns under their team) for review purposes.
- Edit access on returns might be allowed (some firms allow the reviewer to directly fix issues; others prefer sending back to preparer – this can be configurable).
- Ability to mark a return as approved or to lock a return from further editing once finalized.
- Can initiate or send e-file once reviewed (in some setups, only the reviewer/manager files the return).
- Cannot manage global system settings (unless also an admin). Possibly can assign returns or reassign if acting in a managerial capacity.

### 3.3 Firm Administrator

**Description:** The Firm Administrator (Admin) oversees the system configuration and user management for the tax firm’s account. This could be an office manager, the owner of the firm, or an IT lead in a larger firm. They ensure the system is set up correctly for the team.

**Key Responsibilities:**

- Configure firm-wide settings (office information, EFIN – Electronic Filing Identification Number, signing credentials, default preferences like e-file options, fee structures, etc.).
- Manage user accounts: create new user logins for preparers/reviewers, assign roles, reset passwords, deactivate users who leave, etc.
- Set permission levels and assign clients or workflows to users as needed (for example, assign which preparer is responsible for which client).
- Access and manage billing within the software (if the software tracks per-return billing or integrates with vendor billing).
- Monitor overall system usage and status: e.g., view dashboards of how many returns are done, e-files transmitted, rejections, etc.
- Run firm-level reports (like productivity reports by preparer, status of all client filings, etc.).
- Oversee integration configurations: e.g., connect the software to the firm’s QuickBooks account, set up e-signature provider keys, etc.
- Ensure data backups or exports for the firm (in on-prem deployments, they coordinate IT tasks like backing up the database; in SaaS, they might export data at end of season if needed).
- Handle any secure information like IRS registration of software (in case needed) or coordinate with the vendor for support issues.

**Permissions:**

- Full **administrative access** to all data in the system (can view all clients and returns, though they might not typically edit returns unless they also function as a preparer).
- User management rights: add/edit/remove user accounts; assign roles.
- Configuration rights: change settings that affect the whole system or firm.
- Access to audit logs of user activity (they can review the audit trail, see who made changes if needed).
- Initiate or transmit any return (the admin could act as a superuser who can file any client’s return, though in practice they might only do this if stepping in).
- Cannot change audit logs or tamper with certain compliance data (the system should protect the integrity of data even from admin if possible; e.g., admin can’t delete e-file history).
- In an on-prem scenario, the Firm Admin might also have access to system-level settings like database, but those are beyond application scope (that would be IT).

### 3.4 Client (Taxpayer) – External Portal User

**Description:** The Client is the taxpayer for whom the returns are being prepared. Typically, clients don’t log into the tax preparation software directly; however, our system will provide a **client portal** capability. Through this portal or via secure links, the client can perform certain actions to facilitate the process.

**Key Capabilities for Clients:**

- **Document Upload:** Clients can upload source documents (W-2s, 1099s, receipts, etc.) to a secure portal where the preparer can retrieve them. This is an optional workflow to gather data without email. The portal simplifies document sharing and keeps sensitive data secure.
- **Information Review:** Clients may be able to review summary information (like a draft tax summary or their profile info for confirmation). For example, the preparer might share a summary of taxes owed/refund or a copy of the prepared return for client review.
- **E-Signature:** Clients receive notifications when documents are ready for signing. They can log in to the portal or follow a secure link to review the PDF of their tax return or authorization form and apply an electronic signature. Their role in the system is limited to signing or approving documents electronically.
- **Status Tracking:** Optionally, clients could see the status of their return (e.g., “In Progress”, “Filed on 4/10/2025, accepted by IRS on 4/12/2025”) and any messages from the preparer. This reduces phone calls to the office to check “Is my refund filed yet?”.
- **Payment of Fees:** If the firm offers an online payment option, clients might pay their preparation fee through the portal (or indicate they want fee deducted from refund). This could be integrated with an online payment gateway for credit card processing.

**Permissions:**

- Very limited scope: a client can only access their own tax documents and messages.
- They cannot see any other client data or any internal preparer tools.
- They have upload rights for documents to send to the preparer.
- They have read rights to any document shared with them (e.g., a PDF copy of their return).
- They have sign/approve rights only for their documents and only through the e-sign process (which is controlled; they can’t arbitrarily change data – they only review and sign).
- No access to internal menus like e-filing or forms; the portal is a simplified interface separate from the main preparer interface.

**Note:** The client portal is an integrated but separate component for security. Even though clients are “users”, they are external. The system must enforce a strong boundary such that a compromise of a client account cannot affect any other data.

### 3.5 Role-Based Access Control Matrix

To summarize permissions, below is a table of what each role can do within the system:

| **Function / Access**                     | **Tax Preparer**                                      | **Reviewer/Manager**                       | **Firm Admin**                                         | **Client (Portal)**            |
| ----------------------------------------- | ----------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------ | ------------------------------ |
| View own assigned client returns          | Yes                                                   | Yes (all or team)                          | Yes (all)                                              | Yes (own return summary)       |
| Edit/prepare tax return data              | Yes (their clients)                                   | Possibly (for review, or if also preparer) | Yes (any, but typically doesn’t)                       | No                             |
| Create new client records                 | Yes                                                   | Maybe (if allowed)                         | Yes                                                    | No                             |
| Delete client records/returns             | No (to avoid accidental loss)                         | No                                         | Yes (should be rare, perhaps only if created in error) | No                             |
| Submit e-file (transmit return)           | Yes (if policy allows; or requires reviewer approval) | Yes (for reviewed returns)                 | Yes (any)                                              | No                             |
| Initiate e-signature request              | Yes (for their clients)                               | Yes (any client)                           | Yes (any client)                                       | Yes (sign their own documents) |
| Approve/Review returns (mark as reviewed) | No                                                    | Yes (for returns they review)              | Yes (could override)                                   | No                             |
| Manage user accounts                      | No                                                    | No                                         | Yes                                                    | No                             |
| Configure firm settings (EFIN, etc.)      | No                                                    | No                                         | Yes                                                    | No                             |
| Import data (from accounting, etc.)       | Yes (their clients)                                   | Yes                                        | Yes                                                    | No                             |
| View audit logs                           | No (only their actions on their screen)               | No (unless given access)                   | Yes                                                    | No                             |
| View reports (firm-wide)                  | Limited (own productivity maybe)                      | Possibly (team stats)                      | Yes (firm-wide)                                        | Limited (own tax report)       |
| Access via API (if relevant)              | Possibly (with their credentials, for their clients)  | Possibly                                   | Yes (all data)                                         | No                             |

_Table: Role-based access and permissions matrix._

Security and proper role segregation are critical: for example, a preparer should not accidentally access another firm’s data in a multi-tenant scenario, and clients should have absolutely no access to anything except their own information. The system will enforce these boundaries through authentication and authorization checks at every function.

Roles should be configurable to some extent. For instance, a small firm might give all preparers the ability to see all clients (shared pool), whereas a larger firm might assign clients to specific preparers. The software should allow an admin to configure those preferences (e.g., “restrict preparers to their own clients only: Yes/No”).

Additionally, the system should log role-related events in the audit trail (see section 13): e.g., when an admin changes someone’s role or permissions, that should be logged for accountability.

---

## 4. Workflow Overview and Data Lifecycle

Understanding the end-to-end workflow of how data and tasks flow through the system is essential in designing features that align with real-world usage. This section describes the typical lifecycle of a tax return in the system, from the initial client onboarding to final filing and beyond. It also highlights how different roles (from Section 3) interact at each stage.

### 4.1 Client Onboarding and Data Collection

**Client Onboarding:** The process usually begins when a new client (individual or business) engages the tax firm. The system should support adding a new client profile either manually or via an import (if migrating from another system). Key steps:

- **Create Client Profile:** A preparer or admin enters the client’s basic information: name, contact info, tax IDs (SSN/EIN), date of birth (for individuals), filing status (if known), dependent info, etc. For businesses, this includes business type, year-end, owner info, etc. This populates the client database.
- **Engagement Setup:** (Outside the software, the firm might have the client sign an engagement letter; our system could store that as an uploaded document in the client’s file for record, though generation of engagement letters is out-of-scope except maybe via a template).
- **Prior Data Import:** If the client had their prior year return done elsewhere and provides a copy or if the firm is migrating data, the preparer can import last year’s return data. This could be via direct import if coming from a supported format (some standard or using a conversion utility), or by manually keying in prior year summary (like carryovers, depreciation schedules, etc.). The system should allow entering prior-year figures which will be used in current calculations (e.g., prior year AGI for e-file verification, carryover of capital losses, etc.).
- **Document Collection:** Using the secure client portal or in-person, the client provides source documents (W-2s, 1099s, K-1s, receipts for deductions, etc.). If using the portal, the client uploads these files, and the preparer can see them tagged to that client. The system should support organizing these uploads (perhaps by type or just a list of files). If not via portal, the preparer scans and uploads them or stores notes that they have them physically.
- **Questionnaire/Data Intake:** Some tax software includes a questionnaire or interview form to collect information systematically (especially for individual taxes). The system might provide an optional client questionnaire that the preparer can fill while talking to client or even send to client to fill via portal. This ensures all relevant info is captured (for example: “Did you have any crypto transactions? Did you have health insurance all year?” etc.). While not explicitly required, including an **intake workflow** can improve accuracy.
- **Assign Preparer:** If an admin is onboarding the client, they may assign a preparer (or team) responsible for this client in the system so that person gets notified and can start working. In a solo practice, the same person does all roles.

At the end of onboarding, the system should have a complete client record ready for preparation: basic info is in, documents are gathered (or in progress), prior data is available, and the responsible staff is assigned. The next step is actual tax preparation.

### 4.2 Tax Return Preparation Process

This is the core of the workflow where the tax forms are completed and the tax liability or refund is calculated.

- **Data Entry/Input:** The preparer enters the financial data into the software. This can be done via direct form entry (fields corresponding to IRS forms) or via worksheets. For example, the preparer will input wages (from W-2), interest income (from 1099-INT), etc., in the appropriate sections. The software should have a user-friendly interface to input this data. Integration can streamline some of this: e.g., import W-2 details from a payroll provider if available, or import a trial balance from QuickBooks for a business return to populate revenue/expense fields.
- **Real-Time Calculations:** As data is entered, the tax calculation engine computes subtotals, tax, credits, etc. The preparer can see immediate results (e.g., running refund or amount due calculation). This helps them know how inputs are affecting the outcome. The **software automates all tax calculations** (e.g., tax bracket application, credit phaseouts, AMT calculation, etc.), so the preparer does not need to do math manually.
- **Forms and Schedules Generation:** Based on the data, the software determines which forms and schedules are needed. For instance, entering dividend income triggers Schedule B generation; having a capital asset sale triggers Schedule D, etc. These forms are populated in the background. The preparer can review any form in draft mode to see how it looks.
- **Import Data from Integrations:** At this stage, the preparer might use the import features:

  - Pull in data from accounting software for business clients (e.g., import a trial balance to map into a business tax return, or import a list of fixed assets into a depreciation module).
  - Import prior year data to carry over values (like carryover losses, depreciation basis, etc. – some systems allow opening last year’s file and rolling it forward).
  - Fetch data from third-party: maybe import stock transactions from a brokerage CSV, etc., to fill Schedule D or Form 8949 automatically.

- **Preliminary Review & Diagnostics:** Once all expected data is entered, the preparer uses software diagnostics to check for errors or missing info. The system should run an **error check** (for example, ensuring all required fields are filled, values are within expected ranges, certain forms that should be attached are present, etc.). Many professional software provide an “Audit” or “Diagnostics” report showing issues. For example: “Missing Employer ID on W-2” or “Income exceeds threshold, did you input Medicare surtax?” or simple checks like validating SSN format. The preparer addresses any flagged issues.
- **Tax Planning Consideration:** Sometimes at preparation, the preparer might explore options to reduce tax (especially if doing a year-end tax planning or deciding whether to take a deduction vs credit). Our system can support what-if analysis (see section 11) – the preparer could temporarily adjust some inputs in a “scenario mode” to see the impact (e.g., “What if you contributed an extra \$1000 to IRA?”). But in the main workflow, this might be limited; more formal planning is in Section 11.

Now a draft return is ready. The preparer would likely produce a draft summary or even print a draft tax return PDF to review.

### 4.3 Review and Quality Assurance

After preparation, especially in a multi-person firm or for complex returns, a review step occurs:

- **Internal Review by Second Pair of Eyes:** The return can be marked “Ready for Review” in the system. A designated Reviewer or simply another colleague will then go through the return. They will typically look at the input forms, check source documents versus entries (ensuring all provided documents are accounted for in the numbers), and examine diagnostics if any remain.
- **Check Against Prior Year (if available):** The software can produce a comparison report between this year and last year’s return for the client. Reviewers use this to spot anomalies (e.g., income doubled but no note as to why, or a usual deduction is missing this year). The system should have a **year-over-year comparison report** to facilitate this check.
- **Compliance and Reasonability Checks:** The reviewer might use additional tools:

  - Ensure that required forms like the IRS **“Due Diligence Checklist” (Form 8867)** for certain credits are included if applicable (the software should prompt for this if needed, e.g., if claiming Earned Income Credit).
  - Review any overridden values (if the software allows overriding a calculation, it should flag those for review).
  - If the system has integrated research or content, the reviewer might click on a form line to see instructions, but that’s auxiliary.

- **Reviewer Feedback:** If issues are found, the reviewer can either fix them (if minor and allowed) or send the return back to the preparer with notes. The software could have a commenting system or at least allow a status change (“Needs correction”) with notes.
- **Approval:** Once satisfied, the reviewer marks the return as **Approved** or “Reviewed”. This status is recorded. At this point, the return is effectively ready to be finalized and delivered to the client for signature.

In smaller operations, the same person might just self-review using the diagnostics and then move on. The workflow should be flexible to accommodate both formal multi-person review or a single preparer doing all. But the system should support the formal review steps for quality assurance.

### 4.4 Client Review and Approval (E-Signature)

Before filing, the client typically needs to review the return and formally approve it (often via signing Form 8879 for e-file authorization).

- **Prepare Client Copy:** The system generates a final draft of the tax return (PDF format) that can be shared with the client. This includes all forms and schedules that will be filed, and possibly a cover letter or summary. The preparer or admin can use the system to either print this package or, more commonly now, share it via the secure client portal or email a secure link.
- **Client Notification:** Using integrated communications, the system notifies the client that their return is ready for review and signature. For example, the client portal sends an email: “Your tax return has been prepared and is ready for your review. Please log in to review and sign.” Alternatively, the preparer could download the PDF and manually email, but integration is preferred for tracking.
- **Client Review:** The client logs into the portal to view their tax return documents. They can optionally download and save a copy. If they have questions, they might send a message or call – the system could have a messaging feature in the portal to send queries which the preparer sees. (This messaging is a nice-to-have; otherwise, outside communication will be used.)
- **Electronic Signature Collection:** Along with the return, the system will present the client with an e-signature request for necessary forms:

  - **Form 8879 (IRS e-file Signature Authorization)** for each return (federal and possibly state equivalent). The system should fill this form with the relevant information (names, SSNs, amounts) and require the client’s electronic signature. If a joint return, both spouses need to sign (so two signatures).
  - If the firm uses engagement letters or invoices to be signed, those could also be sent for e-sign at this time (though not an IRS requirement, it could be part of firm workflow).
  - The e-signature solution must comply with IRS requirements for remote signature. **IRS Publication 1345 requires identity verification (often knowledge-based authentication questions) if the taxpayer is not physically present** when e-signing 8879. Our integrated e-signature process should include this step: for example, the client may have to answer out-of-wallet questions or input a code sent to their phone to verify identity before signing. This ensures the signature is IRS-compliant (more in Section 10).

- **Signature Audit Trail:** Once the client(s) sign, the system should record the date/time of signature, and retain the signed documents (Form 8879 with an electronic signature stamp, etc.) in the system for compliance. A notification can alert the preparer that the client has signed.
- **Client Approval Complete:** With signatures in place, the client has essentially approved the filing. The preparer can now proceed to final submission. If the client had issues or changes, they would communicate back (perhaps the return goes back to “In Progress” if changes needed, then re-reviewed). The software should allow this loop as needed (maybe with versioning of returns or at least allowing editing until filed).

### 4.5 Filing (Submission to Tax Agencies)

With client approval, the return can be filed:

- **Final Review (Pre-Filing):** It’s prudent that the system runs a final e-file validation check. E-filing has specific technical rules (for example, certain fields cannot contain certain characters, etc.). The software should run an IRS schema validation and business rule check (as per IRS e-file specifications) on the return. Any errors found (like a missing field that wasn’t critical for a paper return but is mandatory for e-file schema) are flagged. The preparer fixes if needed.
- **Generate E-File (XML/Format):** The system converts the tax return data into the format required by the IRS and states. The IRS and most states use the **Modernized e-File (MeF)** system which accepts returns in XML format. Our software will produce an XML submission file per IRS schema for the return, including all attachments required. If any PDFs need to be attached (some forms require PDF attachments for supporting documents), the software will ensure they are attached in the transmission package.
- **Transmit to IRS/State:** The software (cloud version) connects over the internet to IRS e-file servers and transmits the return. This may be done through an integrated third-party e-file gateway or directly if the software is certified as an IRS e-file provider. The system should also handle state filings, either by transmitting through the IRS Fed/State system or directly to states that require direct submission. (The details of each state’s method are handled behind the scenes by the software).
- **Acknowledgment Receipt:** After transmission, the IRS system will process the return and send back an acknowledgment (ACK). There are two main outcomes:

  - **Accepted:** The return passed all IRS checks and is accepted as filed.
  - **Rejected:** The return failed some check (maybe a validation error, or a name/SSN mismatch, or calculation issue) and is not accepted.
  - (Sometimes returns can also be in a “pending” state for a while – the software should account for that and periodically check status via the IRS interface.)

- **State ACKs:** Similar process for states – some piggyback on the federal ACK, others send separate ACKs. The software will gather those too.
- **Notify Preparer:** The system updates the status of the return to Filed-Pending or Filed-Accepted/Rejected accordingly. It should notify the preparer (and possibly the firm admin) when acknowledgments come back. In a cloud system, this can be near-real-time. In an on-prem deployment, the software would connect and retrieve ACKs when online.
- **Handle Rejections:** If a return is rejected, the system should log the error codes and messages from the IRS. These should be presented clearly to the preparer (e.g., “Reject R0000-504: Primary SSN and Name Control do not match IRS records”). The preparer then knows what to fix. The software can even provide guidance or links to what that error means. The return would be moved back to an “Error – Needs Correction” status. After corrections, the preparer resubmits the e-file. The system should allow re-transmission and track the attempts. (If the error cannot be resolved or time is short, the preparer might choose to file by paper, but that’s outside normal flow).
- **Confirmation of Filing:** Once accepted, the return status becomes **Filed/Accepted** in the system. The software should store the acknowledgment details (date/time of acceptance, confirmation number, etc.). This is proof of filing. Optionally, the system could send the client a notification of successful filing (perhaps via the portal or email: “Your return was successfully e-filed and accepted by the IRS on X date”).

For cases where e-filing is not possible (e.g., certain prior year returns or forms that must be paper-filed), the workflow is:

- The software can print an official copy of the return with filing instructions. The preparer would then mail it. The system can mark the return as “Filed by mail” with a date, but no electronic ACK is expected. The document management should allow recording that it was mailed (maybe by logging a note or scanning certified mail receipt).
- But given modern standards, most filings will be electronic (the IRS and many states mandate e-filing for most preparers above a certain volume).

### 4.6 Post-Filing, Support, and Record Keeping

After filing, there are still important workflow elements:

- **Payment and Refund Processing:** If the client owes taxes, the preparer should ensure the client has instructions to pay. The software, during e-file, can include bank account info for direct debit of payment or it can generate payment vouchers. If included (some states allow direct debit in e-file), the acceptance might confirm that the payment is scheduled. The system should record any payment details (amount, date) if provided. If the client is due a refund, and especially if using refund deduction for fees (see Section 12), the software will track the refund status via the integrated bank product partner. Not all software will track the actual refund all the way (that might be via separate bank portals or IRS “Where’s My Refund”), but at least fee collection status is tracked.

- **Amendments and Corrections:** Sometimes after filing, a mistake is discovered or client brings additional info. The system should support preparing amended returns (1040-X for federal, equivalent state amendments). The workflow for an amendment: the preparer opens the originally filed return in an “Amend mode”, inputs changes, and the software generates the 1040-X form with differences. E-filing for amended returns is supported now for recent years, so the system should allow electronic filing of amendments for supported jurisdictions or guide the preparer to paper file if not supported. The original and amended returns should both be stored.

- **Extensions:** If the filing deadline is approaching and the return is not ready, preparers file an extension (Form 4868 for individual, 7004 for businesses). The system should facilitate this easily. Possibly as part of workflow, if it’s April 10 and a client is still missing documents, the preparer can click “File Extension” in the client’s record. The software then generates the extension form, allows input of an estimated payment if needed, and e-files the extension. Then the client’s record is marked as extended until October. This prevents missed deadlines. This extension process is part of compliance workflow (could be in Deadline management features in client management).

- **Record Keeping:** The software should maintain a record of all filed returns. Typically, after filing season, firms archive data but need to retain returns for at least a number of years (often 3 years minimum per IRS guidance, but many keep indefinitely). Our system (especially the cloud version) should store the return data and PDFs securely for future access. The preparer or admin can pull up prior year returns, reprint documents, etc., whenever needed. In on-prem, the firm will have the database – but the software should provide a means to backup/export all returns at end of season (for example, to PDF or a standardized format).

- **Audit Support:** If a client gets audited or receives a notice, the firm will need to reference the filed return. The system’s stored data and documents become crucial. Additionally, features like “Audit Trail” (Section 13) log changes and could help demonstrate due diligence. Some software include a summary of changes or diagnostics that were cleared – useful if defending a position. While actual audit defense is beyond software, having complete records in one place is helpful. (Some products offer an “audit assistance” feature or integrate with services, but at minimum we keep data handy).

- **Client Feedback and Continuation:** After the process, a firm might note lessons or client feedback (maybe in CRM). Our system might not directly handle client feedback beyond storing notes, but from a workflow perspective, the cycle might include a wrap-up step: send client a satisfaction survey or simply mark the engagement complete. Possibly, the system could set a reminder for next year or for quarterly estimates. For example, schedule a task: “send tax planning letter in November” or “remind client to pay Q2 estimate”. These are more practice management tasks, but our system could facilitate via reminders in client record or calendar export.

- **Next Year Rollover:** When the next tax year’s software is available, the firm will roll forward the data. For a cloud system, this might be seamless (the application is updated to new year, and clients carry forward). For on-prem, they might install a new version yearly and migrate data. Regardless, the workflow at year-end involves updating for new tax law and preparing for the next cycle with prior data in place.

In summary, the workflow in our professional tax software follows a clear path: **Client onboarding → Data entry and preparation → Internal review → Client e-sign approval → E-filing submission → Post-filing tasks**. Each step has specific features and requirements in the software to support it, which are detailed in the upcoming sections. This lifecycle perspective ensures that we build features not in isolation, but as part of a cohesive process that product managers and developers can optimize for smooth user experience.

---

## 5. Client Information Management

One of the foundational capabilities of the system is managing client information efficiently and securely. The “client information management” module serves as the database of all clients (taxpayers) and their key data, acting as the starting point for return preparation and a record for future reference.

### 5.1 Client Profile Database

**Requirement:** The system shall provide a centralized **Client Database** where each client (individual or organization) has a profile storing all relevant information needed for tax preparation.

- Each client profile will have a unique identifier and basic fields such as:

  - **For Individual clients:** First name, Last name, Social Security Number (SSN) or Tax ID, Date of Birth, contact information (address, phone, email), filing status (single, married filing jointly, etc.), spouse name/SSN if applicable, dependent details (names, SSNs, birthdays, relation).
  - **For Business clients:** Business name, Employer Identification Number (EIN), type of entity (C-Corp, S-Corp, Partnership, etc.), fiscal year (calendar or other), business address, contact person, and owners/principals info as needed (for K-1 generation or signatures).

- The profile should also store attributes like prior year Adjusted Gross Income (AGI) or a PIN (for e-file identity verification), carryover amounts from last year (capital loss carryover, NOLs, credit carryovers, etc.), which can be automatically pulled into the tax forms.
- **Multiple Tax Profiles per Client:** In some cases, a single individual might require multiple types of returns (e.g., personal 1040 and perhaps they also have a single-member LLC reported on Schedule C, which is still part of 1040 though). For businesses, a business might file multiple returns (e.g., partnership return and a related payroll return, though payroll is out of scope). Typically, one profile corresponds to one return of a given type per year. However, if needed, the system should allow multiple tax files per client per year (though normally one; exceptions could be like filing both federal and a separate local return).
- **Multi-Year Data:** The database should organize data by tax year. For each client, you can have a record of each tax year’s return (with current being in progress and past archived). This allows reference to prior returns easily. It is expected that much of the profile info carries over year to year (to avoid re-entering name, SSN, etc. every year).

### 5.2 Contact and Identity Information (Tax IDs, Filing Status, etc.)

**Requirement:** Capture all necessary identity and status info for accurate filing and compliance:

- **Tax Identification Numbers:** The system must validate the format of SSNs (9 digits) and EINs (9 digits with appropriate formatting) upon entry to reduce errors. These are critical for e-filing (e.g., an incorrectly formatted SSN will be rejected). Possibly include simple checksum validations or known prefixes (IRS has some validation rules).
- **Filing Status & Household Info:** For individuals, filing status is important (Single, MFJ, MFS, Head of Household, Qualifying Widow(er)). The software should allow selecting this and guide what’s needed (if HoH, need a dependent; if MFJ, need spouse info, etc.). It should handle changes year-over-year (e.g., if last year was MFJ but spouse died in current year, qualifying widow(er) might apply).
- **Dependents:** There should be a sub-section in the client profile for dependents, each with name, SSN, birthdate, relationship, and perhaps indicators like if they qualify for Child Tax Credit or not (the software can determine based on age, etc.). This list is used to populate forms like 1040 and to compute credits.
- **For Businesses:** Capture state of incorporation or state nexus if needed (for generating state returns), business code (NAICS code) for the tax return, and officer information for signatures (some business returns require listing an officer and their title, phone).
- **Miscellaneous Profile Data:** Certain returns require specific info: e.g., Driver’s License info for some state e-filings (some states ask for driver’s license number of taxpayer as an anti-fraud measure). The profile should have fields to store such optional info. Another example: bank account info for direct deposit of refunds or debit of taxes due – the system can save a client’s routing/account number (with appropriate encryption) so it can be reused each year if desired.
- **Notes and Tags:** The system should allow adding freeform notes or tags to a client profile. For example, a preparer might note “Client prefers phone contact in evenings” or tag the client as “VIP” or “Extension-filed”. Tags could help filter clients (like see all who are on extension). These do not directly affect tax calculation but are useful for practice management.
- **Client Engagement Info:** Possibly store how the client was acquired or engagement type (e.g., hourly vs flat fee) if that matters for billing. This is secondary, but at least a field for fee charged or invoice reference might be kept.

### 5.3 Client Document Management

**Requirement:** The software should include a basic **document management system** associated with each client, enabling storage and retrieval of files relevant to tax preparation.

- **Upload and Store Documents:** Preparers and clients (via portal) can upload documents (PDFs, images, etc.) to the client’s folder. These could be source documents (W-2s, 1099s, receipts, prior returns), signed documents (e.g., engagement letter, e-file signature form after signing), or any correspondence (IRS notices, etc.).
- **Organize Files:** The system can allow categorization of documents by type or year. For example, a user uploading can label a document as “W-2 2024” or “Client Upload – Medical Receipts”. A simple category system or at least a description field upon upload will help keep order.
- **Storage Limits:** The system should set reasonable file size limits (to prevent huge video files etc.), and possibly a total storage quota per client or firm (especially for SaaS multi-tenant environment, to manage storage costs). For on-prem, it might rely on their storage.
- **Viewing:** Users (preparer, reviewer, and the client for their own docs) should be able to view/download these documents from within the interface easily. Perhaps an in-app PDF viewer for quick look at a W-2 while entering data.
- **Security:** Documents contain PII, so they should be stored encrypted on the server. Access controls must ensure only the client’s preparer team and the client (for their own files) can access them. Proper measures to prevent one client’s docs being accessed by another client or unauthorized user must be in place.
- **Versioning:** If a document is updated (e.g., client sends a corrected document), it might be useful to keep the old version rather than overwrite, or at least allow multiple files (like W2_v1, W2_v2). But a simple approach is fine; versioning is not critical if users can just add new files.
- **Retention:** Perhaps allow the firm to archive or delete documents after a retention period if needed, but by default keep them with the tax return record (most will keep at least 3 years of supporting docs for audit defense).
- **Integration with Preparation:** While entering data, it would be helpful if the preparer can have the source document open side-by-side or easily toggle. Some advanced systems do OCR to auto-read documents, but that is beyond initial scope (though a possible future enhancement: e.g., scan a W-2 to populate fields automatically).
- **Client Access:** Through the portal, clients can upload and possibly download what they uploaded, and see what documents the preparer has shared (like the draft return PDF). But clients likely should not see everything in the preparer’s folder unless explicitly shared (e.g., internal notes or IRS notices might be internal).
- This feature essentially acts as a mini DMS (Document Management System) integrated into the client profile, reducing reliance on external file sharing.

### 5.4 Managing Deadlines and Tasks per Client

**Requirement:** The system should help track key deadlines and statuses for each client’s filings, to ensure nothing is missed.

- **Filing Deadline Tracking:** For each client’s return, the software knows the standard due date (e.g., April 15 for individuals, March 15 for S-corps/partnerships, April 15 for C-corps – unless weekends/holidays shift it). It should display the due date and perhaps a countdown or flag as it approaches. If an extension is filed, it should update the due date to the extended deadline (e.g., October 15).
- **Status Indicators:** Each client return can have a status: Not Started, In Progress, Awaiting Client Info, Ready for Review, Reviewed, Pending Signature, E-Filed (Pending ACK), Completed (Accepted), or Extended, etc. These statuses help the firm manage workflow. The system should allow setting and filtering by status. For example, one could filter to “All clients awaiting signature” to see which clients need a nudge.
- **Task Lists or Checklists:** Some systems provide a checklist of tasks for each return (especially for complex business returns or if following a standardized process). For instance, tasks like “Import QuickBooks data”, “Enter W-2s”, “Review depreciation schedule”, “Send draft to client”, etc. The product could have a default checklist template that can be marked off or even customized by the firm. This ensures consistency in preparation steps.
- **Reminders:** The system might send reminders or have a dashboard for approaching deadlines. For example, show a list: “These 5 clients have not been filed and due date is in 7 days.” Or if a client is on extension, maybe a reminder a month before October deadline. These can be notifications to the preparer or admin.
- **Extensions Filed Log:** Keep track if an extension was filed for a client (and the date, confirmation number if any). So you know they are covered till the extended deadline.
- **Multi-Year Consideration:** If planning for next year, might mark a client as “to carry forward to next year” (which usually all do unless disengaged). Possibly note if a client will not continue, but that’s more CRM.
- **Integration with Calendar/Email:** Not required, but a nice feature could be the ability to sync deadlines or tasks to an external calendar (via iCal feed, etc.) so preparers see key dates in Outlook/Google Calendar. Or the system can send an email reminder to assigned preparer for “deadline coming” or “client X just uploaded a document” etc. Such notifications improve responsiveness.
- **Bulk Status Management:** Admin might need to update statuses in bulk or move many clients to extension. Possibly a screen to mark multiple selected clients as extended and generate all extensions in one go (could be a time-saver for April 15 when extending dozens).
- **Client Portal Integration:** Perhaps the client could also see a basic status, e.g., “Your return is in progress” or “Filed on \[date].” But that’s optional transparency.

In summary, the client info management module ensures we **“manage client information, such as tax identification numbers, filing status, etc.”** and organize everything about the client in one place. It acts as the launching pad for preparing returns, a repository for client data and documents, and a tool to keep track of progress and deadlines for each client engagement.

With robust client management, the software helps preparers handle a large volume of clients without letting any detail slip through the cracks – a necessity for professional tax practices, particularly during the busy season.

---

## 6. Tax Return Preparation & Computation

This section covers the core functionality of creating and calculating tax returns – the bread and butter of the tax software. It details support for various return types, the tax calculation engine, and how the system ensures accuracy and compliance during preparation.

### 6.1 Support for Individual Tax Returns (Form 1040 Series)

**Requirement:** The software must fully support preparation of U.S. individual income tax returns (Form 1040 and related schedules/forms) for a variety of taxpayer situations.

- **Form 1040 and Schedules 1-3:** The core individual return and the common supplemental schedules (Schedule 1 for additional income/adjustments, Schedule 2 for certain taxes, Schedule 3 for non-refundable credits, etc.). The software should automatically produce these based on inputs (e.g., if an adjustment like student loan interest is entered, Schedule 1 is prepared).
- **Schedules for Income:** Support Schedule A (Itemized Deductions), Schedule B (Interest/Dividends), Schedule C (Business income for sole proprietors), Schedule D & Form 8949 (Capital gains and losses), Schedule E (Rental and passthrough income), Schedule F (Farm income), etc. Essentially all schedules that can be part of a 1040 return must be included.
- **Credits and Deductions Forms:** Support all common credit forms: e.g., 2441 (Child Care Credit), 8863 (Education Credits), 1116 (Foreign Tax Credit), 2441, 8880 (Retirement Savers Credit), 8936 (EV credit), etc. Also deduction forms like 2106 (though employee expense misc. might be obsolete), 8917 (tuition deduction if applicable), etc. The software should incorporate the logic for each of these (for example, phaseouts of credits based on income).
- **Other IRS Forms for Individuals:** This includes forms for health care (8962 for ACA Premium Tax Credit, 8965 for exemptions historically), 2210 (underpayment penalty calculation), 6251 (Alternative Minimum Tax), 8949 (detailed stock transactions), 8960 (Net Investment Income Tax), 8959 (Additional Medicare Tax), 1040-ES (quarterly estimate vouchers), among others. Essentially, if the IRS might require it with a 1040, the software should have it available.
- **State Individual Returns:** (Though covered more in Section 7, it’s worth noting here) – for any state a client resides in or has income in, the software should support the corresponding state individual return (and part-year/non-resident forms as needed). Often, data flows from the federal into the state calculations, so integrated support is needed.
- **Multiple Scenarios per Client:** In rare cases, a client might need multiple 1040s in a year (if a preparer is what-if planning or comparing MFJ vs MFS for a married couple). Some software allow having an “MFS scenario” for each spouse separate. While not a core requirement, flexibility to handle scenario analysis is desirable (see tax planning). At least, we should allow easy toggling between MFJ and MFS for calculation without re-entering everything (maybe splitting a joint file into two).
- **Prior Year Support:** The current software version will primarily handle the current tax year. However, professionals sometimes file prior year returns. The product should ideally allow preparing at least one or two years back in the same interface, or provide a backward compatibility mode. This might be handled by keeping old year software available or a multi-year version. (For SaaS, perhaps the app can switch year context; for on-prem, separate programs per year). It’s important to note but maybe beyond immediate scope to fully detail prior-year support except that it’s expected in pro software.
- **Accuracy of Calculations:** The system’s calculation engine must apply all tax rules for individuals correctly:

  - Compute taxable income by summing all income items and subtracting adjustments.
  - Apply correct tax rates (looking up the tax tables or formulas for the filing status).
  - Handle preferential rates (capital gains, qualified dividends) using the appropriate worksheets.
  - Calculate each credit with its specific rules and phaseout thresholds.
  - Ensure that e.g. the Qualified Business Income deduction (QBI, 199A) is computed if applicable.
  - If limitations apply (like deducting only \$10k of SALT taxes, or medical only above certain % of income), those must be enforced.
  - The forms and final numbers should exactly match what a manual preparation following IRS instructions would yield.

- **Adjustments and Overrides:** Provide ability for a knowledgeable user to override a calculated amount if needed (with a warning and audit trail). For example, if a form allows a discretionary input or if there’s a known bug workaround, an override might be necessary. Each override should be flagged so it can be reviewed.

### 6.2 Support for Business Tax Returns (1120, 1120S, 1065, etc.)

**Requirement:** The software must support preparation of common business entity tax returns, as many professional preparers handle small business taxes in addition to individuals.

- **Form 1120 (C-Corporation Income Tax):** Support corporate tax returns including all schedules and attachments (Schedule C, J, K, L, etc. within the 1120, as well as Form 1125-A Cost of Goods Sold, 1125-E Officer Comp, etc.). The calculation must handle corporate tax rates (flat 21% currently), net operating loss rules, dividend received deductions, etc. Also Form 4466 (quick refund) if needed, 7004 for extension, etc.
- **Form 1120S (S-Corporation Income Tax):** Support S-Corp returns including Schedule K-1 generation for shareholders. The software should handle passthrough items and basis calculations if possible. It should prepare the Schedule K and K-1s accurately, and any related forms (e.g., 1120S Schedule M-2 for AAA, etc.). Also apply any limits on deductions at entity level (though S-corps mostly passthrough).
- **Form 1065 (Partnership Return):** Support partnerships/LLCs returns. Must handle allocation of income to partners via K-1s, special allocations if any (some advanced needed for partial). Generate K-1 forms for each partner with all relevant codes for income, deductions, credits. Handle partnership-specific issues like guaranteed payments, self-employment income calculation for partners, etc. Also support attachments like Form 8825 for rental real estate (like a Schedule E for partnerships), and K-1s from other partnerships feeding in.
- **Form 1041 (Estate and Trust Income Tax):** Support fiduciary returns – while less common, many pros do trust returns. This involves calculating income and deductions for a trust or estate and determining distribution to beneficiaries (Schedule K-1 for 1041). The software should handle simple trust allocations vs complex trust, etc., and the specific tax rates for trusts (which are compressed brackets).
- **Form 990 (Exempt Organizations):** Many professional packages include at least basic support for nonprofit returns (990, 990-EZ, 990-PF). It might be slightly less common for a typical tax office, but including it broadens market (some CPAs handle nonprofits). The software should at least allow completing Form 990 and required schedules (A, B, etc.).
- **Other Business Forms:** If positioning as comprehensive:

  - 706/709 estate & gift tax returns might not be in initial scope (they are more specialized, often separate products).
  - 5500 (benefit plan returns) likely out-of-scope.
  - However, Form 941/940 (payroll tax) and sales tax returns are typically not in tax prep software (they are either separate payroll software or done by accountants with write-up software). So those can be out-of-scope except maybe integration points.

- **State Business Returns:** Just as with individual, support state returns for businesses (state corporate income tax, state partnership returns, etc., and local returns where applicable). If a business operates in multiple states, the software should support multi-state allocation/apportionment calculations. Many states require apportionment factors (sales, payroll, property) for multi-state corps – the software should provide a worksheet to input those and compute state taxable income accordingly.
- **Depreciation and Asset Management:** A critical component for business returns is depreciation. The software must include a depreciation module that tracks fixed assets, allows choosing methods (MACRS, Section 179, bonus depreciation, listed property rules) and automatically calculates current year depreciation expense and carryover values. It should produce forms like 4562. It should also keep track of asset depreciation from year to year (so an asset added last year continues to depreciate).
- **Financial Statement Import:** For business returns, often the trial balance from accounting system can be imported. The software should facilitate mapping of trial balance accounts to tax return lines (a mapping for Schedule M-1, M-3 if large corp). Possibly include a worksheet for book-to-tax adjustments (M-1 reconciliation).
- **K-1 Import:** The software should allow that K-1s from other entities can be input into an entity (e.g., a partnership might be a partner in another partnership; need to input that K-1) or for individuals, K-1s feed into 1040. This means supporting all the codes on K-1 forms to properly carry to respective schedules.
- **Error Checking & Balancing:** The system must ensure that balance sheets balance (if required, like for 1120/1065 with > \$ assets thresholds). It should flag if assets != liabilities+capital. And ensure Schedule M-2 (for partnerships and S-corps) properly tracks retained earnings/AAA, etc. Provide diagnostics like “balance sheet out of balance by \$X” for user to fix.
- **Fiscal Year Support:** Unlike individual returns (calendar year), business returns may be fiscal year (e.g., a corp might have July 1 to June 30 fiscal year). The software must support choosing a fiscal year and apply appropriate tax laws for that year (for instance, a fiscal year that spans a tax law change might have special handling). Usually professional software have you select the year of the start of fiscal or end – we need to handle those calculations. Also ensure e-filing works for fiscal year (IRS MeF supports fiscal year by specifying period dates).
- **Printing Forms and Attachments:** All forms, schedules, and K-1s should be nicely printable/PDF. K-1s often need to be delivered to clients of the partnership or S-corp; the system should be able to batch print or PDF all K-1s for distribution.
- **E-filing Business Returns:** Covered in section 8, but ensure that these business forms can also be e-filed (IRS supports e-filing for 1120, 1120S, 1065, 1041, 990, etc.). The software will accommodate any special e-file requirements (like 1065 e-file requires PDFs of certain statements if over certain number of partners, etc.).
- **Calculations Accuracy:** All business tax calculations must be correct according to tax law:

  - For C-corps: correctly compute tax, any credits (general business credits, etc.), any limitations (e.g., 163(j) interest limitation).
  - For S-corps/Partnerships: ensure no tax at entity (except state franchise taxes or built-in gains for S-corps etc.), but allocate items properly.
  - For 1041: handle distribution deductions, throw income between beneficiary and trust appropriately, etc.

By including all these business forms, our software distinguishes itself as a **professional suite** rather than a simple individual-only preparer. Many professional firms indeed handle both individual and business clients, and having them in one software increases efficiency (and is expected – leading packages like Intuit Lacerte, Drake, CCH Axcess, etc. include all these). The G2 criteria explicitly mentions the ability to “calculate and file individual or business tax returns”, which we cover by supporting the above.

### 6.3 Tax Calculation Engine (Automated Calculations)

**Requirement:** The system shall include an automated tax calculation engine that computes all tax values in real-time or on-demand, minimizing manual calculations by the user.

- **Real-Time Recalculation:** As data is entered or changed, the software should recalc the affected fields. For example, entering a new W-2 wages amount immediately updates the total income, tax, and refund amount. If not real-time, at least a “Recalculate” button that quickly updates is needed, but modern systems do it continuously or whenever you navigate.
- **Linkage of Fields:** Many tax form lines are interdependent. The engine must link fields appropriately. E.g., entering data in Schedule D feeds into 1040 line for capital gains, which might feed into the Qualified Dividends and Capital Gain Tax Worksheet. The engine needs to handle iterative dependencies (like if a credit depends on tax which depends on credit – usually done via worksheets).
- **Completeness of Tax Logic:** The engine should encapsulate logic from IRS instructions and tax code:

  - Phaseouts: e.g., Child Tax Credit phases out after income X – engine should reduce the credit accordingly.
  - Limitations: e.g., charitable deduction for a corporation limited to 10% of income – engine should apply automatically.
  - Alternative Minimum Tax: if applicable, compute AMT by its own set of rules and take the higher of regular or AMT.
  - Refundable vs Nonrefundable: ensure credits categorized properly and any excess flows to refund or not as appropriate.
  - Form selection: if an entry triggers a less common scenario, ensure the correct form is included. (For instance, if foreign taxes paid > \$300, then Form 1116 is required instead of taking the automatic credit).

- **Speed and Performance:** The calculation engine must be optimized for speed, as preparers will be entering data quickly and expecting instant results even on complex returns. The system should handle even large datasets (like a partnership with 100 partners or 1000 stock trades) without significant lag. Performance requirements are detailed in Section 16, but the engine should ideally handle normal returns in fractions of a second and even large ones within a few seconds at most.
- **Accuracy and Testing:** The engine should be tested against known scenarios and IRS test cases. (The IRS ATS testing gives a set of scenarios that the software must produce correct results for). The product team will maintain a library of test returns to validate calculation accuracy whenever tax law changes or new code is written.
- **Override Mechanism:** Provide ability to override calculated values in rare cases (with caution). When a user enters an override, the engine should stop computing that field and use the override value. It should flag that field as overridden so it isn’t accidentally left overridden (especially year to year). Overrides might be needed for things like force an amount due to some manual adjustment or when following specific instructions (sometimes IRS instructions allow a different approach).
- **Rounding and Precision:** Ensure standard rounding rules (usually to nearest dollar on tax forms, with .50 up rounding up) are applied consistently. If currency is in cents internally, round only at final output. Also, state forms sometimes require different rounding (some to nearest dollar, some to nearest cent, rarely).
- **Multiple Calculations (Filing Status or Scenario):** The engine should be able to handle scenario comparisons like Married Filing Joint vs Married Filing Separate – possibly by duplicating data into two profiles or an internal scenario mechanism to calculate both and compare liabilities. This is a feature in some software to advise which status is beneficial. Not a core requirement but nice to have in planning tools.
- **Constant Updates:** The calculation engine’s rules must be updateable each tax year (or mid-year if tax law changes mid-year). The architecture should separate data (like rates, thresholds) from code logic, making it easier to update annually. For SaaS, updates will be rolled out centrally; for on-prem, an update mechanism to apply patches or new year modules is needed.
- **Support Manual Calculations Attachments:** Some complex things can’t be fully computed automatically without additional input. For example, say a very unusual tax situation might need a manual worksheet that the preparer completes and then enters a result. The software should allow that (maybe attach a PDF of a custom calc and override a field). But we aim to minimize such cases by including as much logic as possible.

Overall, the engine ensures that **tax preparation is streamlined with high accuracy**, one of the selling points of professional tax software. By automating all math and logic, we reduce human error and speed up the process significantly.

### 6.4 Compliance Rules and Error Checking

**Requirement:** The system must have robust compliance checking features to ensure returns are accurate and adhere to IRS and state e-filing rules before submission.

- **Real-Time Validation:** As data is entered, certain validations can trigger immediate warnings. For example, if a user enters an obviously invalid value (like letters where numbers expected, or an unreasonable age for a dependent), the field could show an error.
- **Diagnostics/Alerts Summary:** The software should compile a list of issues that need attention. This might be accessible via a “Check Return” function that the preparer runs when nearing completion. Diagnostics should cover:

  - Missing required data: e.g., “Dependent SSN missing” or “Business code (NAICS) not entered for Schedule C.”
  - Contradictory answers: e.g., “Filing status is Single but a spouse SSN is entered.”
  - Threshold warnings: e.g., “Medical expenses entered but total is below 7.5% AGI, they won’t affect Schedule A” – not an error, but possibly an informative note.
  - E-File compliance: e.g., “Name contains invalid character & which is not allowed in e-file, please remove.”
  - Critical calculations: e.g., “Schedule M-1 does not balance – difference is \$500.”
  - Tax law flags: e.g., “Income over \$X with no estimated tax payments entered – check for penalty form.” (some software are smart to prompt adding Form 2210).

- **Interview or Guide Mode (Optional):** While professionals often use forms directly, an optional interview mode could guide through common questions and ensure nothing is missed (like an organized Q\&A that covers life events, etc.). However, this might not be heavily used by pros who prefer direct control. Still, some checks can mimic that: e.g., if a taxpayer is over 65, prompt “Did they receive Social Security? If yes, ensure SSA-1099 is entered” as a friendly reminder.
- **Tax Law Updates and Compliance:** Each year, the system must incorporate the latest tax law changes (new credits, expiring provisions, inflation-adjusted thresholds). For example, if a credit’s expiration means it no longer applies in the current year, the software should not offer it or should show it's expired. Or if new forms are introduced (like a new Schedule for a credit), it should be included. Compliance includes not only calculations but also adherence to IRS e-file schemas (which change year to year).
- **Regulatory Checks:** If there are preparer compliance requirements, e.g., if a due diligence form (Form 8867) is required when claiming certain credits, the software should enforce that. It should not allow e-filing a return claiming Earned Income Credit without a completed 8867, as the IRS would reject that or penalize the preparer. So the software safeguards the preparer by requiring those forms.
- **Review Checklists:** Possibly provide a checklist of common issues for reviewer to manually check as well (though not enforced by software, just guidance).
- **State/Local Compliance:** Each state may have its own rules or quirks. The system should incorporate state diagnostic checks as well. E.g., warn if a city return is needed when a certain city is in the address (like NYC resident needs NYC tax form as part of NY return).
- **Updates via Internet:** The compliance rules might need updates when IRS issues notices or corrections. The software should be able to receive updates (for SaaS, automatically; for desktop, via patch downloads). For example, if Congress passes a late tax law change in December affecting the filing season, an update must be issued to reflect that. Similarly, if an IRS schema update happens, update e-file rules accordingly.
- **Internal Consistency and Math Checks:** Even though calculation engine handles math, the diagnostics should double-check critical consistencies:

  - Sum of details equals summary line (e.g., sum of all W-2 wages entries equals wages on 1040).
  - Refund/payments cross-check: if a refund is large compared to income, maybe a note to double-check entries (this could catch some keying errors).
  - Social Security numbers consistency (if spouse SSN appears in two places, must match).

- **Pre-Efile Audit:** Before allowing e-file submission, the software should require that there are no outstanding critical errors. It may allow informational warnings to remain (with confirmation) but not errors that would cause rejection. This gatekeeping prevents wasting time on rejected submissions.

By building in these compliance and error-check mechanisms, the software acts as a safety net, ensuring preparers catch mistakes. This is crucial because IRS rejections or client dissatisfaction from errors can be costly. Professional tax software is expected to provide **“error-checking”** features as noted in industry descriptions, which reduces the chance of rejections and audits.

### 6.5 Handling Tax Law Updates

**Requirement:** The system must be designed to handle annual (and occasional mid-year) changes in tax laws, forms, and rates with minimal disruption to users.

- **Annual Update Process:** Typically, professional tax software goes through an update cycle each year for the new tax filing season (often referred to as a new “program” for the tax year). Our system should incorporate all changes for Tax Year 2025 (for example) in time for filing season (usually by December or early January). Changes include:

  - New tax rates or bracket thresholds (which are indexed for inflation).
  - Standard deduction changes, credit limits, retirement contribution limits, etc.
  - Form changes: If IRS adds, removes, or revises forms, the software must reflect that. For instance, in 2021 the 1040 had a new question about cryptocurrency – software had to add that field.
  - Expiring provisions: e.g., if a credit expired last year, remove it or hide for current year.
  - New laws: e.g., if a new deduction for certain businesses is introduced, incorporate that (new form or new line on existing form).

- **Internal Architecture for Updates:** Ideally, much of the form logic and data (like tax rates, thresholds) should be data-driven or configurable so that updating does not require rewriting entire modules from scratch. The system can store tables of rates or use formula configurations that are loaded per tax year.
- **Testing New Law:** Each update should be thoroughly tested, including running known scenarios from previous year under new rules to see expected differences. The system might include an internal simulation feature to verify calculations (some companies use thousands of test returns in the update QA process).
- **Mid-Year Changes:** Occasionally, laws change mid-year or retroactively. The system should allow patching calculations and forms even during the filing season. For example, if Congress extends a deduction retroactively in late January, an update must be issued quickly so returns can include that. The software should handle versioning such that returns already started may need to be recalculated (with user notification).
- **State Updates:** Multiply the above by 50 states. Each state releases its forms on slightly different schedules, often after federal. The software must update state forms and calculations as they become available. Usually, initial release might have draft state forms and later update final versions. The system should alert users when final forms are ready and not allow final filing until forms are finalized/approved (to avoid using draft).
- **E-File Schema Updates:** The IRS and states also update the electronic file schemas annually. Our e-file subsystem (section 8) must be updated accordingly. The system should enforce using the correct tax year schema for each return. It might automatically select the appropriate one based on year of return.
- **Compliance with ATS Testing:** Before release, the updated software must pass IRS Assurance Testing (ATS) for each tax year, meaning all test scenarios are filed without error and accepted by IRS. This is an internal process, but product managers ensure it’s scheduled. The requirement is that the software cannot be considered compliant or safe for e-filing until it passes those tests and is approved by IRS for that year.
- **User Notification:** When using the software, users should easily tell what version (and tax year) they are in. The software should display the tax year being prepared, and if an update is pending or available. Possibly provide release notes for significant changes so preparers know if something new is supported or if they need to take action (like review any partially prepared returns for changes).
- **Backward Compatibility:** Data from previous years should carry forward into the new year seamlessly (with conversion if needed). For example, if a 2024 return exists, when starting 2025 for that client, it should auto-import carryovers. If a law change affects a carryover (e.g., carryover rules changed), handle it accordingly (maybe alert the preparer if needed).
- **On-Premise vs Cloud Updates:**

  - In the cloud deployment, updates will be applied on the server side. The system might roll out updates during off-hours; users might log in one day and get a message “Tax tables updated to 2025 values” or similar. We should avoid downtime, but if needed, schedule minimal downtime (section 16 covers availability).
  - For on-premise, provide update installers or patches that the firm’s IT can apply. Ensure they are easy to apply and won’t corrupt existing data. Possibly an auto-update feature if the server has internet access to pull updates.

- **Support for Multiple Years Concurrently:** Some firms might be filing prior year returns alongside current year. The software ideally should allow use of prior-year modules. In a cloud scenario, perhaps a user can choose tax year context when starting a new return. In on-prem, separate installations for each year are common. We should clarify how our design handles multi-year:

  - One approach: A single application that can handle multiple tax years by selecting year (especially if web-based).
  - Another: Separate instances per year. This might complicate data carryover.
  - It might be easier in initial design to focus on current year and perhaps one year back. This is more of an implementation decision.

- **Regulatory Changes beyond Tax Law:** If IRS changes e-file rules (like requiring new authentication steps, or new security requirements), our software must adapt. For example, IRS could mandate multi-factor authentication for software providers or new data encryption standards – these must be incorporated timely.

By adeptly handling tax law updates, we ensure the software remains **compliant with the latest laws and IRS standards**, which is non-negotiable in this industry. This is part of regulatory compliance (section 16.3) but directly impacts functional behavior too. Product managers will schedule annual development cycles aligned with government release calendars to ensure timely updates.

---

## 7. Tax Forms Coverage (Federal, State, Local)

This section details the requirement of supporting a wide range of tax forms at the federal, state, and local levels. Comprehensive form coverage is one of the distinguishing features of professional tax software, as preparers need to handle various jurisdictions and scenarios.

### 7.1 Supported Federal Forms and Schedules

**Requirement:** The software shall support all commonly required federal IRS tax forms and schedules for individual and business filings in scope.

As summarized earlier, the key federal forms include (but are not limited to):

- **Individual (1040) Series:**

  - Form 1040 and 1040-SR (for seniors) – including all standard Schedules (A, B, C, D, E, F) and additional schedules (1, 2, 3).
  - Supporting forms like 2441 (Child & Dep Care), 8863 (Education Credits), 1116 (Foreign tax credit), 6251 (AMT), 4797 (Sale of business property), 8949 (capital gains details), 8959/8960 (additional Medicare tax / NIIT), 8962 (Premium Tax Credit), 8379 (Injured Spouse), etc. Basically, if it can attach to a 1040, it should be present.
  - Specialized forms: e.g., 2555 (Foreign Earned Income Exclusion), 3520 (Foreign trusts, if we include? Possibly not common, but some pros need it).

- **Business (1120/1120S/1065):**

  - Form 1120 (C-Corp) and schedules, 1120-W (estimated tax for corp), 5471 (if dealing with foreign subs – advanced, may skip initially), 8975 (country-by-country report – only large corps, could skip).
  - Form 1120S and Schedules K-1 for S corp, 1120S K-1 statements.
  - Form 1065 and Schedules K-1 for partnership, plus related like 1065 K-3 (international things, if applicable).
  - Common forms for entities: 4562 (Depreciation, as mentioned), 4797, 8949 (entities can have capital assets too), 3800 (General Business Credit), 6252 (Installment sales), 5472 (foreign owner of US corp), etc.

- **Estates/Trusts & Others:**

  - Form 1041 and K-1s, plus 1041-T if needed (allocation to beneficiaries), 5227 (split-interest trusts).
  - Form 990 series: 990 (long), 990-EZ, 990-PF and schedules (A, B, C... etc. There's many schedules for nonprofits).
  - Gift/Estate (709, 706) – likely out-of-scope for initial product but if included, that’s additional forms.

- **Employee Benefit forms (5500)** – usually not included in tax prep software, so we can consider out-of-scope.
- **Amended Returns:** 1040-X for individuals, and equivalent for business (1120-X for C-corp, but actually rarely used as many corp amendments can be just 1120 with check box, but support if needed; 1065 and 1120S often use 1065X or just refile K-1s as amended via 1065 with box checked). We should provide a way to generate amended returns and the forms needed.
- **Extensions:** Form 4868 (individual extension), Form 7004 (extension for businesses and trusts etc., which covers 1120, 1065, 1041, 990 via checkboxes). Those should be easy to produce and e-file.

The software should include **all IRS forms necessary to cover the needs of typical individual and small business clients**, which effectively means hundreds of forms. Professional packages often support upwards of 2,000 forms. We might not list each one here, but our design assumes any form that a preparer might need is available. The G2 criteria mentions “multiple tax forms across federal, state, and local tax programs” as a qualification, so broad coverage is a must.

### 7.2 Supported State and Local Tax Forms

**Requirement:** The software shall support state tax returns for all U.S. states (and DC) that have income tax filing requirements, for both individuals and businesses, as well as common local tax forms where applicable.

- **State Individual Income Tax Forms:** For each state with a personal income tax, provide the main tax return form (e.g., CA 540, NY IT-201, IL 1040, etc.) and all supporting schedules/attachments for that state. This includes part-year and non-resident returns (often separate forms or schedules). Ensure support for credits and adjustments specific to each state.

  - E.g., California has numerous subforms (CA Schedule CA for adjustments, Schedule D for state capital gains differences, etc.), New York has IT-2 for W-2 summary, and so on. The software should handle state additions/subtractions from income, different credit calculations (like CA has its own EITC).

- **State Business Tax Forms:** For each state that taxes corporations, S-corps, partnerships, trusts:

  - Corporate tax returns (e.g., CA 100 for corps, NY CT-3, Illinois IL-1120, etc.).
  - S-Corp returns at state level (some states piggyback, others have separate forms).
  - Partnership returns (many states require a partnership informational return, often with K-1 equivalent for state).
  - State fiduciary returns (for trusts/estates).
  - Include state-specific forms like Texas franchise tax, Ohio CAT (commercial activity tax) if in scope. Possibly, those are on the edge but important for completeness in certain states.

- **Local Tax Forms:** Some local jurisdictions have income taxes, notably:

  - New York City and Yonkers (part of the NY state return forms).
  - Various city taxes in Ohio (often these are separate from the state system; supporting Ohio municipalities could be a huge task as there are many forms – some pro software integrate with a third-party service for that. We may at least provide generic support or the major ones).
  - Pennsylvania local Earned Income Taxes (administered by local tax bureaus).
  - Detroit city return, etc.
  - We should aim to support the major localities either directly or via available modules, but perhaps not every small municipality initially. Possibly integrate or allow manual form fill for less common ones.

- **No-Tax States:** States like Florida, Texas (for personal), etc., have no personal income tax. The software can indicate "No state return required" for those. But they might have business franchise taxes (e.g., Texas franchise, Washington B\&O). It’s a decision whether to include those as they are somewhat different from income tax. Ideally, at least mention coverage: perhaps support Texas Franchise and maybe NYC Unincorporated Business Tax, etc., to cover major cases.
- **DC and Territories:** Include Washington DC individual and corporate returns. U.S. territories (Puerto Rico, Guam, etc.) usually have separate systems – likely out of scope except maybe a Guam mirror code, but probably skip territories in initial.
- **Forms and E-Filing:** For each state, ensure that forms can be printed and also e-filed if the state supports e-filing (most do, often via the federal MeF gateway or separate). The software should implement state e-file specifications. Some states piggyback on IRS e-file (you send state data embedded with federal), others require separate transmission. We'll handle that in e-file section, but our forms data structure must accommodate state-specific electronic filing data (which can differ from printed form).
- **Localization:** The software should apply state-specific rules accurately. For instance:

  - Different definitions of income: e.g., states that don’t tax certain income or add back others (like muni bond interest from other states).
  - State credits for taxes paid to other states (for residents with out-of-state income).
  - Composite returns for partnerships (some states allow a composite filing for nonresident partners, the software should support generating that).
  - City tax integration: e.g., in NYC, tax is part of NY return form.

- **State Estimates and Extensions:** Support state extension forms (most states accept the federal extension or have their own form) and state estimated tax vouchers (for quarterlies).
- **Updates and Maintenance:** State forms change yearly too. The system must update each state’s forms and calculations. Often states release later than IRS, so initial release might have some states pending. We will have to deliver state form updates as they become available (e.g., maybe by early January have most states, some late changes might come as patches).
- **Volume of Forms:** There are dozens of forms per state potentially. We likely need to ensure the development plan covers building out each state’s form set and testing them. Possibly prioritize high-population states (CA, NY, TX for franchise, FL for intangible if any, etc.) then others. But ultimately, to compete, we need “All States Included” which TaxSlayer and others advertise. Preparers expect not to have to use a different software for one state.
- **Multi-State Handling:** Provide support for allocating income to states for nonresident returns. E.g., someone lives in NJ but works in NY: the software should allow preparing both, auto-calculate credit for taxes paid to NY on NJ return. Partnerships with multi-state income: allow entering apportionment factors and have the system generate state K-1s if needed or at least state composite returns. This is complex but necessary for business returns that operate in many states.
- **Local integration:** Possibly include integration or guidance if local returns are not fully handled. For example, if an Ohio city return is needed, and if not fully in software, at least inform the user and maybe link to a resource. But ideally, include them to avoid manual work.

The aim is that a firm using our software can serve clients from anywhere in the country with any state obligations without resorting to separate tools. That’s a major selling point (advertised as “All States Included, free unlimited e-filing” by many).

### 7.3 Annual Updates to Forms and Rates

_(This overlaps with 6.5 Tax Law Updates, but here focusing specifically on forms)_

**Requirement:** Ensure all forms (federal and state) and tax rates/tables are updated each year, as part of the tax law compliance:

- Each form’s layout and line numbers must match the official government forms for that tax year. If IRS renumbers lines or adds a new line, our form views reflect that.
- The software’s printouts must be acceptable to file (for paper filings) – typically meaning they look very close to official forms. Most software generate a facsimile of the official form with data filled in. For e-file, the exact look is less important, but we should still produce a human-readable copy that matches the official form format, for client copy or record.
- **IRS Forms Approval:** The IRS and states sometimes require software vendors to get forms approved (for print accuracy, scannable forms etc.). Our team will submit samples to IRS/state if needed to get form approval numbers. This is internal compliance but relevant to quality.
- **Tax Tables and Rates:** Update standard deduction, personal exemption (if it existed, currently 0 but in future maybe returns), tax brackets, contribution limits, mileage rates (if we have any calculation for auto expenses), per diem rates if relevant, etc. Many of these are in IRS revenue procedures each year.
- **New Forms:** If a new credit or deduction is introduced with its own form, the software should include it. E.g., if a new form 1099-NEC appears (like it did in 2020 to replace 1099-MISC for non-employee comp), ensure integration of that input. Or new schedules like Schedule 8812 changed in 2021 for ACTC.
- **Removing Forms:** If forms are obsoleted (like 1040-NR-EZ was discontinued, or 1099-B instructions changed something), ensure removed.
- **State and Local Changes:** States may change tax rates or add/remove credits each year (like one year a state might have a one-time rebate). The software should adapt to those changes. Possibly allow some state-specific configuration if a small locality changes something that we can parameterize rather than code anew.
- **Quality Assurance:** After updates, thorough testing with test cases and perhaps cross-verification with other sources (like run a scenario in old version vs new to see correct changes, or compare with IRS’s own calculations if possible).

This annual update process is a significant yearly project for any tax software and must be planned well in advance (monitoring draft forms, etc.). We already covered the process in 6.5; 7.3 just reiterates the necessity with respect to forms.

### 7.4 Extension and Amended Return Support

**Requirement:** Facilitate filing of extensions and amended returns, which are common needs for professional preparers.

- **Extensions:**

  - As mentioned, support Form 4868 and 7004 (and any state extension forms if separate). The software should allow generating an extension for a client with minimal input (largely just name, SSN/EIN, and an estimate of tax liability if needed).
  - It should carry forward any currently input data to estimate tax due for extension (or allow manual override of amount paid with extension).
  - Provide an option to electronically file the extension (IRS accepts e-filed 4868 and 7004).
  - Mark the client as extended and perhaps prevent filing a final return until after extension (just logically, or at least indicate extension filed).
  - If extension is filed via our system, store the acknowledgment of that as well.
  - For tracking, maybe list extension clients so none are forgotten after deadline.

- **Amended Returns:**

  - Provide a mode to prepare an amended return. There are two approaches:

    1. **In-place amendment:** Some software have a toggle "Amended return" and allow you to enter original figures vs new figures and it computes differences. For 1040-X, for instance, columns A (original), B (net change), C (corrected). The software should ideally auto-fill column A from the originally filed return (if it was done in the software) and allow editing to reflect changes. Then it generates Form 1040-X with the differences. Similarly for 1120-X (or 1120 with Amended box), 1065 (amended K-1s).
    2. **Duplicate & Modify:** Another method is to copy the original return data into a new instance, make changes, and then the software compares the two and generates the X form.

  - In either case, we need to output the required amended return form and any corrected schedules.
  - E-filing amended: Historically not always available for all forms, but IRS now allows e-filing 1040-X (for recent years) and some states do. The software should support e-filing amendments where allowed (and default to paper where not).
  - Keep a link between original and amended. Possibly track multiple amendments if done (like Amended #1, #2).
  - If the original was done elsewhere but they want to use our software for amendment, allow user to input original figures manually to produce the X.

- **Supplemental Forms for Amendments:** Some states have their own amendment forms (or simply require refiling with a mark). The software should handle those as well. For example, California Schedule X for amendments, or New York IT-201-X, etc.
- **Carryover Effects:** If an amendment changes a value that carries to next year (like a change in NOL), ensure that is updated for carryover. Possibly prompt user to update the next year’s data or automatically propagate if within same software. But careful not to override if next year already filed. Some logging needed.
- **Notice Responses:** Slightly related: If a client gets an IRS notice (CP2000, etc.), preparers often need to recompute something. While not a formal “return”, perhaps the software can be used to simulate the correct figures. We might not specifically build a feature for notice response, but being able to modify data and see impact is helpful.
- **Protecting Filed Data:** When an original return is filed and accepted, it might be good to “lock” that data to avoid accidental changes. Then if amendment needed, require an explicit action to amend rather than just editing a filed return inadvertently. This keeps the record of what was originally filed intact.
- **User Workflow:** Provide clear workflow: e.g., an “Amend Return” button that opens the process. Similarly an “File Extension” button to handle extension easily.

Having strong extension and amendment capabilities is important in professional context since many clients file extensions (complex or late info clients), and corrections are a fact of life. The software should make these tasks as painless as possible, saving time compared to manual form filling.

---

## 8. Electronic Filing (E-Filing) Process

E-filing is critical to modern tax preparation. This section details how the software will handle the end-to-end electronic filing process for federal and state returns, ensuring compliance with IRS and state requirements and providing a smooth experience for users.

### 8.1 E-File Preparation (Data Packaging in IRS Format)

**Requirement:** The software must convert completed tax returns into the appropriate electronic format ready for transmission.

- **Modernized e-File (MeF) XML:** The IRS (and states via MeF) require tax returns to be formatted in XML according to specific schemas for each form type. Our software will have an **XML generation module** that takes the internal data and produces an XML file conforming to the IRS schema for that year and form.

  - The schema dictates the structure: e.g., an element for each line item, with certain data types. We must ensure all required elements are present and optional ones are included if applicable.
  - This includes bundling of all forms and schedules in one file (federal and possibly state attachments).

- **Validation Against Schemas:** Before sending, the software should validate the generated XML against the IRS provided XSD schema and business rules. This catches any structural issues early. We might integrate the IRS schema definitions so the software doesn’t produce invalid format.

  - IRS also publishes “business rules” (error codes) for content (e.g., if a certain credit is claimed, another form must be present). Many of these we catch in error checking, but some might be double-checked here.

- **Attachments (PDFs):** Some returns require PDF attachments for certain statements or elections that are not standardized fields. The software should allow attaching PDFs to the e-file submission as required. E.g., if claiming a certain tax treaty position, attach a PDF explanation. Or large charitable contribution statements. The module must incorporate these into the transmission package per IRS guidelines (often as binary attachments referenced in the XML).
- **State Packaging:** If states are piggyback (most are), the state return data is included in the federal XML (often an XML snippet or PDF attached per state specs). If a state requires separate submission, the software may create a separate state XML for that state’s gateway.
- **Encryption/Preparation for Transmission:** Data should be prepared securely. The IRS transmission often happens over secure web services. We must ensure any encryption or signing of the payload is handled (though typically IRS uses TLS for transport; the data itself may not need encryption beyond that, but ensuring no tampering).
- **Multiple Returns:** The software should handle transmitting multiple returns in one session (batch filing). But each return’s data stands alone in its file. Possibly allow bundling but likely one by one. However, from user perspective, they might select 10 returns and hit transmit; the software then loops sending each.
- **EFIN and ETIN info:** The electronic file will include identifiers for the ERO (Electronic Return Originator) – likely the firm’s EFIN (Electronic Filing ID Number provided by IRS when they enroll as e-file provider). Also preparer info and if third-party transmitter, an ETIN.

  - The software should prompt the admin to enter the firm’s EFIN and preparer PTINs in settings. These are inserted into each e-file submission in the proper fields (e.g., the XML has elements for EFIN, and for each prepared return, the PTIN of preparer goes in the appropriate spot on form 1040 data).
  - The system must ensure these are present; otherwise IRS will reject (you cannot e-file without EFIN in the file, typically).

- **Signature Elements:** For e-filed returns, the taxpayer’s signature is basically the presence of the Form 8879 and a PIN. The IRS e-file requires an Authentication Record, which includes e.g. a Self-Select PIN or Practitioner PIN, taxpayer birthdate, prior year AGI or a practitioner PIN with an ERO signature. We need to handle this:

  - The software can use the Practitioner PIN method: the ERO (preparer) sets a 5-digit PIN for taxpayer, taxpayer signs 8879, the ERO signs as well, then that PIN is entered in the e-file XML along with ERO’s EFIN/PIN. That constitutes the electronic signature.
  - Alternatively Self-Select (taxpayer chooses a PIN and provides prior AGI). But in professional context, often Practitioner PIN is easier.
  - Our software should support both, but likely defaults to Practitioner PIN method. It should gather the necessary info (DOB, prior AGI if needed, etc.).
  - These signature elements are included in the e-file package as per IRS requirements, so that a separate physical signature isn’t needed to be sent to IRS (just keep form 8879 on file).

- **Batch Assembly:** Possibly allow an option to “queue” multiple returns and then send them in batch (which is mostly a UI detail). Under the hood, it will iterate creation of each file and sending. For performance, maybe multi-thread if sending many at once.
- **Tracking Data:** Each e-file package should be associated with the client record along with a unique ID (Submission ID) that IRS assigns for tracking, which we will use to query status.

### 8.2 Transmission to IRS and State Systems

**Requirement:** The software shall transmit the prepared e-file data to the IRS (and state agencies) securely and reliably, using the appropriate protocols.

- **Connection Method:** The IRS MeF system is web-based and typically uses Simple Object Access Protocol (SOAP) with web services over HTTPS. We will integrate with the IRS’s e-file API endpoints (there are endpoints for SubmitReturn, GetAcknowledgment, etc.).

  - For a SaaS solution, this integration will be done from the server side.
  - For on-premise, the software needs to connect out to IRS. We must ensure connectivity (the user’s network must allow it). Provide configuration for proxy if needed.

- **Transmitter Identification:** If we act as our own transmitter, we might need an IRS-issued Transmitter Control Code or ETIN. In many cases, tax software companies become IRS Authorized e-file Providers (both as software developer and transmitter). We should plan to do that (Product will need to meet IRS requirements and get a code). Alternatively, some software piggyback on a third-party transmitter service. But likely we will have our built-in system.
- **Security:** Use TLS 1.2/1.3 for encryption in transit. Use IRS provided certificates if required. Ensure the data is sent only to official IRS endpoints (test vs production endpoints accordingly).
- **State Transmissions:** Many states use the IRS Fed/State system (meaning you send to IRS, IRS forwards to state). Others use the Fed system but you need to retrieve state ACK from IRS, etc. A few (like New York, Massachusetts) might require direct submissions or additional steps. The software should handle those behind the scenes:

  - Possibly using separate web service calls to state systems or sending embedded in federal. We will incorporate state e-file guidelines accordingly.
  - For simplicity, at first, if fed/state combined works for majority, use that, and list exceptions we handle specially.

- **Confirmation of Submission:** Once transmitted, log a record that it was sent, including date/time, to whom (IRS, and any state).
- **Handling Transmission Errors:** Sometimes, transmissions fail due to network issues or IRS downtime. The software should catch those exceptions and inform the user so they can retry. Possibly implement automatic retry logic for transient failures.

  - If IRS returns an immediate reject (bad format, etc.), that will come as an ACK with errors rather than a network error. So difference: network error vs logical reject. Network errors we can retry; logical rejections go to user to fix data.

- **Transmission Receipts:** The IRS system typically immediately (or quickly) returns a receipt (like an HTTP 200 with a Submission ID, or an acknowledgment that it's received and pending). Store that submission ID in our database associated with the return.
- **Batch Transmission:** If sending multiple, ensure no mixing of data. Possibly throttle if IRS has limits (e.g., maybe not sending more than X per minute). Possibly abide by any IRS guidelines for volume (since some large providers send tens of thousands in peak hours).
- **Deadlines:** The software should be aware of e-file cutoff times (for instance, typically midnight of deadline day, but in practice, keep track of timezone issues). Also, after the end of filing season, IRS shuts down to update for next year (the software should reflect when e-file opens/closes for a year).
- **Extension Transmission:** Similar process, often a separate endpoint or same with a flag. Just ensure it’s done correctly.
- **On-Prem Note:** If installed locally, ensure the user's environment can perform these transmissions. We might need to supply guidelines (like open specific firewall ports).

By handling transmission, we fulfill the requirement that the software provides **“e-filing options”** and actually carries out the filing.

### 8.3 Acknowledgment Handling (Accepted/Rejected)

**Requirement:** The software shall retrieve and process acknowledgments from tax agencies indicating whether an e-filed return was accepted or rejected (or other status).

- **Acknowledgment Retrieval:** After submission, the IRS system processes returns. The software should periodically check for acknowledgment updates. Two ways:

  - **Synchronous response:** Sometimes IRS might immediately return a reject if schema validation fails. That can be caught right away as a rejection ACK.
  - **Polling:** For normal processing, the software should poll the IRS MeF system using the Submission ID to see if it's accepted or rejected (or still pending). This can be done at set intervals (e.g., every few minutes, or allow user to manually refresh status).
  - The IRS also offers a push mechanism via their message queue (if subscribed). Initially, polling is simpler to implement.

- **Accepted Case:** If accepted:

  - Mark the return in the system as **Accepted** for federal (and similarly for state if separate ACKs).
  - Record the acknowledgment details: date/time of acceptance, acknowledgment number, etc. Possibly store the entire ACK message in case needed.
  - Notify the user (could be a popup or a status icon turning green). Possibly also notify via email or dashboard for overview.
  - For some states (which piggyback), IRS might provide the state acceptance or rejection as part of the federal ACK or shortly after. Ensure to parse those and mark state status as well (e.g., Fed accepted, State X accepted, State Y rejected, etc. can happen).

- **Rejected Case:** If rejected:

  - Mark return as **Rejected** in system (and possibly attach the reject code(s) and descriptions).
  - Display the error messages to the user in a clear manner. Each reject comes with codes and text. The software can translate common codes to friendly explanations. E.g., error IND-046: “The Primary SSN in the Return Header has been locked because Social Security Administration records indicate the number belongs to a deceased individual.” – show that message clearly.
  - Provide guidance or a link to knowledge base for certain errors if possible. At least ensure the user knows which part of the return caused it (maybe highlight the field).
  - Allow the user to go back into the return, fix the issue, and then **resubmit**. The system should allow resubmission after a reject. Possibly require changing the electronic signature PIN or mark as corrected as IRS rules may or may not require (generally can just resend after fix).
  - Track number of attempts. If multiple rejections, keep history. This can help support if something consistently fails.

- **Other Status:** Sometimes acknowledgments can be “Duplicate” (if a return was filed twice), or "Suspended" (rarely, if IRS holds for manual review), or "Partial Accept" (like state accepted, federal rejected or vice versa). The software should handle these gracefully:

  - Duplicate submission: notify user that IRS thinks it's already filed (maybe they accidentally sent twice).
  - Suspended: probably rare in MeF, but if it happens, advise to contact IRS.
  - Partial: highlight which part is accepted and which rejected.

- **State Acks:** For states, similarly retrieve and interpret. Possibly states send codes we need to map. Usually, if through Fed, the IRS provides them.

  - If a state reject occurs but federal accepted, the return might need only state correction. Software should allow re-filing state while keeping federal as accepted.

- **Acknowledgment Storage:** All ACKs (accepted or rejected) should be stored so that if needed, the firm can produce proof of timely filing or see history. Possibly generate an "EF Status report" or printout for record.
- **Client Notification:** Optionally, after acceptance, the system could generate a client letter or email: “Your return was accepted by IRS on X date.” Many pro software can create a generic letter for clients for file. We can template a letter that uses ACK date and other info to confirm filing to client for their peace of mind.
- **Re-file Cutoff:** If rejected after deadline, but originally timely sent, IRS typically considers it timely if fixed within a window (usually 5 days grace for rejected returns to be re-filed). The software might inform user of such rules: e.g., “This return was originally transmitted on 4/15 and rejected. You have until 4/20 to re-submit and still be considered timely.” This is a helpful feature for compliance.
- **Audit Trail:** Log which user transmitted and received acknowledgments. If multiple staff, an admin might want to know who filed what.
- **Summary Dashboard:** Provide a view of e-file statuses across clients (so the firm can see how many accepted, how many rejected/pending at a glance, possibly filter by date or responsible staff).

This acknowledgment processing ensures that the system closes the loop on e-filing. Getting an acceptance is crucial; if something is rejected, our software’s job is to help the preparer correct it quickly. This aligns with being a full-service professional tool that doesn't stop at submission but ensures completion.

### 8.4 Error Resolution and Resubmission

(This is partly covered in 8.3 but to emphasize the workflow for fixing errors.)

**Requirement:** Facilitate easy correction of rejected returns and resubmission without duplicating effort.

- When a rejection occurs, the error message should pinpoint which part of the return caused it. For example, an error might say a dependent’s SSN is already used on another return (IND-518). The preparer should then:

  - Open the client’s return (which the software should allow even though filed, since it's rejected).
  - Go to the dependent section and perhaps see a flag or highlight on that dependent. Correct the issue (maybe get a correct SSN from client or mark as not a dependent if they cannot claim).
  - The software should keep all other data intact – only changes the user makes. No need to re-enter entire return.

- After correction, the user triggers **re-transmit**. The software should ideally re-use relevant info (like the original Submission ID is now moot, a new one will be generated).

  - Possibly must update the signature date in the file (some software automatically update the 8879 signature dates or use the original date – IRS is okay as long as within certain time). Ensuring compliance here is necessary (with Practitioner PIN method, usually if the return data changed materially, one could argue a new 8879 signature might be needed from taxpayer if tax liability changed. Strictly, yes they should resign if something changed. Our system might at least warn if an amount changed: “If the refund/tax due changed, you should get a new signed 8879 from client.” We leave that to the firm’s policy).

- The resubmission is then treated as a new submission to IRS. We track it as another attempt. After sending, again await ACK.
- If the same error comes back, then the issue wasn’t fixed or is external (e.g., if dependent SSN is legitimately claimed by ex-spouse, client can’t override that; they'd have to paper file or remove dependent). The software can’t fix that scenario except advise.
- **Common Reject Assistance:** Possibly have a knowledge base of common rejections and how to resolve:

  - E.g., IND-031: AGI mismatch – instruct user to check prior year AGI or use alternative (maybe use EFIN/PIN instead).
  - If possible, integrate these tips into the error message or link to a support article.

- **Alternative Filing if Unresolvable:** If certain rejections can’t be resolved (like IRS won’t accept electronically due to some data conflict), the software should inform the preparer that they may need to paper file for this client. Perhaps provide an option to mark the return as “Needs to paper file” and then allow printing official forms (with a watermark removed).

  - This should be last resort since e-filing is mandated for preparers (if a preparer files many returns, IRS expects e-file unless excepted). But there are exceptions like the dependent issue where two e-files conflict, one might end up paper.

- **Rejection of Extensions:** If an extension was rejected (maybe name/SSN mismatch), same process: fix and resend until accepted or if not possible, advise paper extension submission.
- **Grace Windows:** As noted, IRS often has a grace period for rejected returns to be considered timely if fixed quickly. The software should highlight that for time-sensitive ones (like near April 15 or October 15).
- Possibly show a countdown or note “Must be accepted by X to avoid late filing.”
- **User Interface:** Maybe present an "E-File Center" where all returns with issues are listed and can jump directly to fix. Some software have separate e-file management screens where you double-click a reject and it opens the return to the right place.
- **Resubmission Limits:** In theory, a return can be retransmitted many times. We should allow it until accepted or the user aborts. But if like 5 rejections, maybe recommend to file by paper to avoid further delay (some errors won’t clear electronically).
- **Audit trail on changes:** If a return was changed after filing, the audit log should note changes made post initial filing.

### 8.5 E-File Status Tracking and Notifications

**Requirement:** The system should provide clear tracking of e-file status for each return and send notifications of important status changes.

- **Status Dashboard:** There should be an interface (like an “E-file Dashboard” or statuses on the client list) showing each client’s e-file status:

  - Not e-filed (or paper filing status).
  - Transmitted (pending ACK).
  - Accepted.
  - Rejected (with maybe a color red icon).
  - Could also show "In Progress" if currently open for editing or "Awaiting Signature" if we've held off filing.
  - For extensions, perhaps separate indicator.
  - Filter by status: e.g., show all rejected or all pending.

- **Notifications to Users:**

  - In-app notifications: e.g., a pop-up or alert bell when new ACKs come in, especially rejections.
  - Email or SMS (if configured): For example, an admin might want an email "All e-files accepted" summary daily, or immediate email if a reject occurs (so they can act quickly).
  - Configurable in settings which events trigger emails. At minimum, an option for critical rejects.

- **Client Notifications:** As mentioned, possibly an automated email to client on acceptance. Some firms might want that. Could template: "Your return was e-filed on X and accepted on Y. Thank you." The system would mail it out or put a message in client portal.
- **Historical Reports:** Provide the ability to generate reports of e-filing. For instance, number of returns e-filed by date range, list of rejections and resolutions, etc. Useful for firm to review efficiency or provide to IRS if audited (IRS can audit preparers for e-file compliance and will check if they are filing most returns electronically if required).
- **Resend and Recovery:** If a user accidentally clears a status or if they need to retrieve an old ACK, allow re-downloading acknowledgments from IRS (the IRS might allow retrieving historical ACK within the season).
- **Multiple Year E-file:** If supporting multiple years concurrently, clearly separate status by year. E.g., client X might have 2024 return accepted and 2025 in progress. The dashboard should reflect year of return for clarity.
- **States status integration:** Show state statuses along with federal. Possibly as separate line or combined. E.g., "Fed: Accepted, NY: Accepted, NJ: Accepted" or if one is pending, show accordingly.
- **Real-Time Refresh:** In SaaS environment, could use push notifications or refresh to update statuses without user manually clicking. Possibly integrate with a message queue or long poll to update the UI as soon as ACK arrives.
- **Mobile/Remote Access:** Though not required explicitly, some might want to check statuses on the go. If we have a web portal, the user can log in from anywhere to see statuses. Maybe not a separate mobile app at first, but ensure responsive design perhaps so they could check on a tablet/phone if needed.

### 8.6 IRS and State E-File Compliance (ATS Certification)

**Requirement:** The software must adhere to all IRS and state e-file program requirements and undergo necessary testing and certification.

- **IRS Developer Program:** We must follow IRS Pub 3112 and related documents for software developers. Key compliance items:

  - **Assurance Testing System (ATS):** As noted, before each filing season, run through IRS test scenarios for each form type. Ensure the software produces correct results and formats. Only after passing do we get the green light to distribute e-file capability.
  - The requirements include testing certain volume of scenarios: e.g., multiple scenarios for 1040, business, etc.
  - The software should have a mode to generate the test returns (maybe internal; not exposed to users).

- **EFIN usage:** Ensure the software captures the ERO’s EFIN in each return and that only authorized EROs use the software to transmit. Possibly include in the software license that user must have an EFIN to e-file (IRS requires paid preparers who e-file to have one). Could prompt for it in setup and validate length etc.
- **Security of E-File Data:** IRS might require certain data encryption or not storing certain data after submit. For example, the software should not store the full unencrypted submission in a way accessible to users for PII safety. Or if storing, ensure encrypted at rest. More in Security section.
- **State Certification:** Some states require separate certification for software (often piggyback on IRS tests for state portions, but some have their own test scenarios too). We need to comply with any state testing, e.g., California FTB or New York might have test cases or registration.
- **Error Code Updates:** Keep up with any new IRS reject codes or state codes each year, updating the software’s internal library so that messages are up-to-date.
- **Timely Transmissions:** IRS e-file runs typically 24/7 except maintenance; the software should ideally be available to transmit whenever. If cloud, plan maintenance accordingly (as per availability in NFR).
- **User Agreement to e-file rules:** Possibly have the user sign/agree that they will follow IRS e-file rules (like get 8879 signed before transmitting, keep it on file for 3 years, etc.). The software could display a reminder of these responsibilities to help the firm stay compliant as an ERO.
- **Logging per IRS Regs:** IRS might require logging of submissions. Ensure we keep a log of what was sent (without storing sensitive info unnecessarily) to show compliance if needed.
- **Reject Handling:** Already covered, but important as part of compliance is making sure errors are handled properly and not bypassing any rules.
- **Updates to IRS Systems:** IRS occasionally updates their MeF system endpoints or protocols. The software should be designed to be adaptable (e.g., easy to change service URLs, incorporate new authentication tokens if they implement them).
- **Volume Limits:** If IRS imposes any volume constraints (rare, but maybe they throttle if volume too high), our system might need to queue. For normal operations, thousands of returns can be filed; should design to handle high throughput by scaling horizontally if needed.

By meeting all these standards, our software will be an **Authorized IRS e-file Provider** software. Professional tax preparers rely on that – they cannot use a software that is not approved for e-filing, since the IRS will not accept returns from unapproved software. Thus, successful ATS testing and compliance is a go/no-go criterion for the product launch each year.

_(As a note in the PRD, mention that internal teams will coordinate submission of software to IRS for testing and obtaining necessary credentials in advance of tax season.)_

---

&#x20;_Figure: System Context & Integration for Professional Tax Software._ This diagram illustrates the high-level architecture and integration points. The **Professional Tax Software** (center) interacts with various external entities: tax preparers and firm admins use the system to input data and manage returns; client data can come in via an accounting system import or prior year import; clients use a portal to provide documents and sign returns (through an integrated **E-Signature Service**); once returns are approved, the software transmits filings to the **IRS & State e-File systems**, and can handle **Bank/Payment Gateway** interactions for refund transfers and fee collection. Each of these flows is detailed in requirements above, ensuring the system seamlessly ties together all parts of the tax preparation lifecycle.

---

## 9. Data Import and Integration

Integration capabilities are a key part of the software’s value proposition, allowing data to flow in from other systems and sources. This reduces manual input and errors. Below we specify integration requirements, particularly focusing on importing data from accounting platforms, previous returns, and third-party sources.

### 9.1 Import from Accounting Platforms (e.g. QuickBooks)

**Requirement:** The software shall integrate with popular accounting/bookkeeping platforms to import financial data for business tax returns.

- **Supported Platforms:** Initially, focus on QuickBooks (Desktop and Online, since it's widely used by small businesses). Also consider Xero, Sage, FreshBooks, or CSV import for generic use.
- **Data to Import:** For a business entity, the primary import is typically a **Trial Balance** or summary of accounts from the accounting system. This provides totals for income, expense, assets, liabilities, etc., which correspond to lines on tax forms.

  - For example, import total revenue, COGS, various expenses (salaries, rent, etc.) which map onto Schedule C or Form 1120 line items.
  - If the accounting system has tax-specific mapping (QuickBooks allows marking accounts with tax lines), use that mapping for direct import. If not, we provide a mapping interface.

- **Import Process:**

  - **Authentication:** The user should be able to connect the software to their accounting system account. For QuickBooks Online, use Intuit’s API (OAuth, etc.) to get access to the company data. For QuickBooks Desktop, perhaps support import of exported files (like a QuickBooks Trial Balance report CSV or use their SDK if possible). Possibly allow direct reading of QuickBooks files via an SDK for on-prem use.
  - **Company Selection:** If the user has multiple companies in their accounting app, let them choose which one corresponds to the tax client.
  - **Date Range or Year Selection:** Ensure the data aligns with the tax year (fiscal year support if needed). Possibly let them pick the fiscal year in QB to pull.
  - **Mapping to Tax Lines:** Provide a mapping UI where accounts from the accounting chart are listed and the user can assign them to tax return categories if not automatically mapped. Save this mapping for future imports (so next year it’s easier).
  - Possibly integrate standard mappings: e.g., many chart of accounts have obvious mappings (Sales -> Income, Utilities -> Utilities expense line).
  - **Import Schedules:** Some details like fixed asset depreciation might not come from the P\&L if they only have book depreciation. The software might import the fixed asset list for depreciation calculations. If QuickBooks has an asset list, we could pull purchase dates, cost, accumulated depreciation to then run tax depreciation in our module. This could be a deeper integration or could rely on user to provide that separately. For initial, focus on P\&L and balance sheet items.

- **Post-Import Review:** After import, show the user a summary of what's been imported and where. They can adjust any classification if needed. For example, maybe they want to reclassify some expense for tax purposes (like move some expenses to Schedule M-1 adjustments).
- **Updating Data:** If the user changes data in the accounting system, they should be able to re-import or refresh. Or if small changes, they can edit in our software too. We might not want a constant sync (as that can get complicated), but at least allow them to re-run import to update figures if not filed yet.
- **Audit Trail:** Mark imported values in the workpapers so user knows which fields came from integration vs manually entered. Possibly store the raw imported trial balance for reference.
- **Security:** The integration uses secure API calls. Store minimal credentials (in case of OAuth tokens, store encrypted). Respect data confidentiality. If a user disconnects the integration, remove tokens.
- **Other Systems:** Provide at least CSV import as a fallback: e.g., user can upload a CSV of trial balance which our system can parse with mapping to tax fields. This covers any accounting system (they can always export to CSV).
- **Potential Reports:** After tax adjustments, consider exporting adjusting journal entries back to accounting system (some software do this: once you finalize tax depreciation which differs from book, you can push an entry to QB for tax adjustments or for provision if needed). This is a nice-to-have for bookkeeping integration, but possibly advanced beyond MVP.

By integrating with accounting software, the system can significantly reduce time for preparers working on business returns and ensure accuracy by pulling data directly. This aligns with the idea of syncing with accounts to import transaction data automatically.

### 9.2 Import of Prior Year Returns and Data

**Requirement:** The software shall facilitate importing data from previous years’ tax returns, whether prepared in our system (carryforward) or from other tax software, to pre-populate the new return.

- **Carryforward from Our System:** If the prior year’s return was done in our software, the new year’s preparation should automatically carry forward relevant info:

  - Basic client info (name, SSN, etc.).
  - Dependent lists.
  - Prior year adjusted gross income (for e-file verification).
  - Carryover amounts: e.g., capital loss carryovers, charitable contribution carryovers (for C corps), net operating losses, AMT credit carryforward, passive loss carryforwards, basis information for assets, etc.
  - Depreciation schedules: bring over assets with their remaining basis and accumulated depreciation to compute current year depreciation.
  - State carryovers similarly (like state NOL, etc.).
  - Last year’s state refund (which may be taxable in current year).
  - The software should clearly list what it carried over and allow review.
  - Items that need confirmation (like if last year’s return had an overpayment applied to this year’s estimated tax, carry that as a credit and mark accordingly).

- **Import from Different Software:** Many firms switch software or have new clients who bring prior returns done elsewhere. The system should provide ways to import data from:

  - **Standardized formats:** If an interchange format exists (not widely, but some use TXF for trades, not so much entire returns). There is no universal format for full tax returns, unfortunately.
  - **PDF Import:** Some advanced solutions can read a PDF of last year’s return prepared by another software and extract key data (OCR or if PDF has embedded text). We might not implement full OCR initially, but possibly integrate with a service or allow user to enter summary prior data manually on a “Prior Year Data” worksheet.
  - **Manual Entry Worksheet:** Provide a screen where user can input prior year key figures (AGI, taxable income, state refund, carryovers, etc.) if they can’t import directly. This at least collects needed info for current calculations.
  - **Data Conversion Tools:** If possible, provide converters for popular software like converting a TurboTax or Lacerte data file to our format. This is complex but maybe through partnerships or if those software export some format. Many companies do offer data conversion utilities for onboarding new customers. For this PRD, note that “conversion from competitor software will be supported for at least basic data (client info and carryovers)” as a goal.

- **IRS Data (Transcripts):** A forward-looking feature: The IRS provides taxpayer transcripts (via e-Services or new API). Possibly, with client consent, import some data from IRS transcripts (like last year AGI, certain carryovers). This might be advanced and require the firm to have POA or use IRS APIs (which are still evolving). We mention it as potential integration to consider if resources allow.
- **Ensure Accuracy:** After import, present a “Proforma Report” summarizing what came from last year. Preparer should verify it. For instance, if capital loss carryover is imported, show last year schedule D to confirm.
- **Handling Changes in Tax Law Year-over-Year:** If a carryover type no longer exists or changes behavior (like carryback rules changed), handle appropriately or flag. E.g., if a credit carryover expired, warn that it won't carry forward.
- **Efficiency:** The goal is that a returning client’s data entry burden is minimized. The preparer should not re-type names, SSNs, addresses, or re-enter static info. Also, multi-year projects like depreciation should smoothly continue.
- **Amended Return Integration:** If last year's return was amended, ideally carry from the amended figures, not original. That requires tracking which data to use. Could let user choose to import original vs amended as base.

A smooth carryforward process saves huge time and is expected – professional software always includes prior year rollovers for continuity. It ties into user retention (makes them less likely to switch out as well, ironically, but we need it to attract those switching to us).

### 9.3 Third-Party Data Sources (Payroll, Financial Institutions)

**Requirement:** The system should allow importing data from various third-party sources such as payroll providers or financial institutions to populate tax forms (where feasible).

Examples and specifics:

- **W-2 Import (Payroll)**: Many payroll companies (ADP, Paychex, Gusto, etc.) can provide W-2 data electronically.

  - The software could integrate via API or at least allow import of standard W-2 formats (like CSV or EFW2 files).
  - The IRS also has a system (Business Services Online) where you can pull W-2 info if given authorization (though that might be more for SSA use).
  - Simpler: If the client uses an online portal that exports W-2 as CSV, allow mapping fields to our W-2 input.
  - Or allow scanning a W-2 (OCR). Some solutions do this by allowing to take a picture of W-2 and it fills in fields. We might not build our own OCR now, but could consider integrating with a service that OCRs common forms.

- **1099 Import**: Clients with many brokerage transactions (stock trades) often get a consolidated 1099 (1099-B) with potentially hundreds of trades. Manually entering is impractical.

  - Provide import for 1099-B transactions via CSV or broker exports. Many brokers allow download of transactions in CSV or TXF (Tax Exchange Format) which is an old but used format for trades. We should support TXF import to populate Schedule D/8949.
  - For interest/dividends (1099-INT, 1099-DIV), those can also be imported from bank/broker if they provide a file or via integration like Plaid, or Intuit’s financial data APIs (but direct integration might be beyond initial scope).
  - Alternatively, integrate with aggregation services or allow user to forward a data file.

- **K-1 Import**: If a client receives many K-1s from partnerships, etc., the preparer must input each box. If those K-1s were produced by certain software, maybe they can provide a file. Not common for K-1 to have a standardized import, but at least our system should allow copying K-1 data forward if same partnership each year.

  - Possibly allow scanning a K-1 PDF or using an import template for K-1 data if the partnership can export to Excel.

- **1098 Import**: Mortgage interest statements – maybe less critical as usually one or two, easy to type. But could allow reading if provided electronically (like some banks allow downloading interest info).
- **Foreign Account Data**: For FBAR or Form 8938, if client has many accounts, maybe import from a spreadsheet.
- **APIs and Partnerships**: We might consider partnering with an aggregator like Yodlee or Plaid to fetch financial data for tax purposes. E.g., linking a client's investment account to fetch transactions automatically. This is advanced and data-heavy, and would require careful matching to tax categories. Possibly beyond initial scope, but something for value-add.
- **Standard Formats**: Encourage standards: TXF for securities, maybe Excel templates for others.
- **User Experience**: Provide import wizards for these. E.g., "Import Stock Transactions: Upload your brokerage CSV or connect to \[Broker]" wizard. After import, show summary (X transactions imported, Y were short-term, Z long-term).
- **Error Handling**: If a file is not formatted right, give clear error or allow user to map columns manually.
- **Security/Privacy**: Importing financial data is sensitive. Use encryption and ensure data is only used for that client's return. If connecting via credentials (like linking a bank account), ensure use OAuth flows and do not store credentials.
- **Manual Data Entry Minimization**: The overall aim is to reduce the tedious data entry of forms the client already has digitally. The more we integrate, the faster preparers can do complex returns (especially those with many documents).
- **Limitations**: Not everything will have an import. The user should always be able to enter manually if needed. The software should not force integration but offer it when it saves time.

### 9.4 APIs and Data Exchange Mechanisms

**Requirement:** Provide APIs or other data exchange interfaces for advanced integrations and custom workflows.

This section addresses making the system extensible:

- **Public API for Data:** A set of RESTful APIs (with authentication) could be provided for:

  - Creating a client and sending client data into the system (instead of using UI, e.g., from a CRM system).
  - Getting client data or tax results out (for use in another system, like a financial planning app).
  - Pushing documents in or pulling them out.
  - Triggering e-file submission or checking status via API (maybe for large accounting firms that want to integrate with their management systems).
  - Essentially, anything the UI can do, consider an API for automation. This is not typical for all smaller firms, but larger firms or third-party developers might use it.

- **Use Cases for API:**

  - A bookkeeping system could push year-end financials directly to the tax software via API instead of manual import.
  - A client-facing portal (maybe the firm has their own) could integrate via API to create a client in tax software and upload docs.
  - A mobile app could connect to show client status by calling API.

- **Security for API:** Use OAuth2 for third-party access. Possibly only allow the firm’s own integration rather than open public (depending on business model). If open, documentation needed, sandbox keys, etc.
- **Import/Export Data Formats:**

  - Provide an export of the tax return data in a structured format (like XML or JSON). This could be useful if the firm wants to use data for analysis, or to switch software (we should be somewhat open, as it’s user’s data).
  - Possibly allow export of the return as TXF for use in personal finance, though TXF is limited to trades etc.
  - At least allow PDF export of forms (that’s given, for printing).

- **Integration with Practice Management:** Many firms use practice management software for tracking projects (like Karbon, Jetpack Workflow, etc.). If we have an API, those could mark a task complete when a return is marked filed in our system by fetching status, etc.
- **Webhooks:** Alternatively or in addition to polling APIs, we might implement webhooks (outgoing calls) to notify external systems of events (e.g., when a return is accepted, call a URL that the firm’s system listens to).
- **Modular Design for Add-ons:** If third parties want to build add-ons (like a specialized form calculator, or integration with a local tax), a robust API or plugin system could help. For now, likely not, but good to keep architecture in mind (like separation of concerns).
- **Data Import/Export for Archival:** Offer ability to export all client data at end of year for the firm’s archival (some firms like to own their data outside vendor lock). Could be a bunch of PDFs or a database export. Since it’s SaaS, we should provide that as a courtesy if requested.

While building a full API is a significant undertaking, including at least basic data exchange capabilities future-proofs the software for integration in complex environments and larger firms. Given product manager audience, highlighting API potential shows we consider the software as part of a larger ecosystem.

---

## 10. E-Signature Functionality

Integrated e-signature is a major convenience feature that allows clients to approve tax returns remotely and paperlessly. This section details how e-signatures will be incorporated and managed, including compliance aspects.

### 10.1 Integrated E-Signature Workflow

**Requirement:** The software shall provide built-in electronic signature capabilities for obtaining required signatures (primarily taxpayer and spouse signatures on tax forms such as e-file authorizations) within the application.

- **Forms to Sign:** Commonly, Form 8879 (IRS e-file Signature Authorization) for individual returns, and equivalent forms for business e-filing (e.g., 8879-S for S-corp, 8879-PE for partnership, etc.) need signatures. Also possibly engagement letters or Form 2848 (Power of Attorney) if the firm uses them. But initial focus on e-file authorizations.
- **Sending for Signature:** Once a return is ready for client approval (Section 4.4), the preparer can trigger an e-signature request. The software will generate a PDF of the documents to sign (e.g., the 8879 with all fields filled) and any accompanying docs (like a copy of the tax return if you want them to sign acknowledgment of review).
- The client receives an email with a secure link to a signing portal (this could be our client portal, or a standalone signing page).
- The signing interface should be user-friendly: show the document, allow the client to adopt a signature (draw or choose a font), and apply it where needed. If spouse also needs to sign, support multiple signers (two signers on one doc).
- **Signature Completion:** Once signed by all required parties, the system marks that signature task complete and stores the signed PDF in the client's documents.
- **Notification:** Notify the preparer that signatures are done (so they can proceed to e-file).
- **Multiple Attempts/Reminders:** If client delays, system should allow sending reminders or a new link if original expired. Possibly links expire after X days for security.
- **Esignature Provider vs In-House:** We might integrate an existing e-signature solution (like DocuSign, Adobe Sign, or a specialized tax e-sign like CCH eSign) behind the scenes via API. Alternatively, build a simple custom one in-house using open libraries for signature. For time, integration with a known provider might be faster, but cost is a factor. Regardless, from user perspective it's seamless.
- **Embedding in Portal:** If we have a client portal, the sign process can be embedded when they log in – "Please sign the authorization form" with a one-click sign.
- **Audit Trail:** The e-sign system should generate an **audit log** for the signature, detailing when the email was sent, when opened, which IP or device signed, etc., to prove authenticity if needed. This is often provided by e-sign providers. Store that log or certificate with the signed doc.
- **Signing Other Documents:** The firm might also want the client to sign the prepared return itself (though IRS doesn’t require that if e-file, but some clients do sign the Form 1040 as a formality or for their records). Could allow adding additional sign fields on PDF of 1040 for client if requested, though not required by IRS. Focus on what's required legally first (8879).
- **Sign for Business Entities:** For a corporate return, an officer needs to sign 8879-C or the return. We handle similar way, sending to that officer (could be the same portal or an email specifically to that person).
- **Bank Documents:** If using bank products for fee deduction, those usually require an application signature too. Possibly integrate those forms for signature as well in the workflow (like bank product agreements).
- **Experience**: The integrated solution should be smooth enough that it’s easier than printing and scanning. Clients can sign via phone, tablet, or computer – so ensure the signing interface is mobile-responsive.
- **Volume**: The license might allow unlimited e-signs or have a cost per signature depending on provider deals. If any cost constraints, build into pricing model but not a technical req.

By having integrated e-sign, we deliver on the requirement to “obtain client signatures” digitally, eliminating a major bottleneck in tax prep (no more chasing paper).

### 10.2 Compliance with IRS E-Sign Regulations

**Requirement:** The e-signature implementation must comply with IRS and legal standards for electronic signatures on tax documents.

- **IRS Guidelines (Pub 1345):** The IRS allows electronic signatures for Form 8879 and similar forms, but requires identity verification for remote transactions (when taxpayer is not in person). Specifically:

  - The taxpayer’s identity must be verified through knowledge-based authentication (KBA) or certain alternative methods if signing remotely.
  - The e-signature must capture certain details like a timestamp and an IP or unique identifier.
  - The signed form must be tamper-evident (so after signing it shows if altered).
  - The ERO (Electronic Return Originator, i.e., the preparer) must retain the signed 8879 for **3 years** and be able to produce it to IRS on request.

- **Knowledge-Based Authentication:** To comply, our e-signature workflow should integrate KBA questions for the taxpayer(s) if required. Typically, a third-party service provides this by asking questions from public records (like credit history, previous addresses). This could be part of a signing provider’s offering or a separate integration.

  - Possibly have two modes: if the taxpayer is present in office, no KBA needed (they can sign on a signature pad or device under preparer supervision – some consider that in-person e-sign). If remote, use KBA.
  - The threshold: if not applying KBA, IRS may not treat it as an electronic signature and require scanning of a wet signature. So to fully leverage e-sign remotely, we incorporate KBA as needed.

- **Audit Trail Document:** After signing, generate a completion certificate that shows the signer's name, how identity was verified, signature image or hash, date/time, etc. This is evidence that meets IRS standards.
- **Consent Forms:** Under ESIGN Act, the client may need to consent to electronic records/signature. The system should present a consent disclosure at first use for client to agree (for example: "By proceeding, you consent to use electronic records and signatures."). Log that consent.
- **Secure Storage:** The signed forms must be stored securely (encrypted) to prevent tampering. Our audit trail should ensure any change invalidates the signature.
- **No Alteration of Signed Data:** Once 8879 is signed, the tax data on it (like the amount due/refund) should not change. If the return changes, a new form should be generated and re-signed. The software should enforce that (lock return or warn user).
- **IRS ERO Responsibilities:** The software can help ERO meet their responsibilities:

  - ERO must sign the 8879 as well (they can sign electronically too, possibly by just checking a box that they have a PIN on file – in Practitioner PIN method, the ERO's PIN and date is included). We should capture preparer signature/PIN in the process too.
  - Provide a way for preparer to digitally sign forms like 8879 as ERO. Typically, they have an ERO PIN that goes in the e-file. The 8879 requires their signature – which can be electronic as well.

- **Compliance Logs:** Possibly output a report or have data ready if IRS audits the e-sign procedures. Keep records of KBA questions outcome (pass/fail, not the answers obviously, just that it was done).
- **State Compliance:** Some states also allow e-signature on their equivalent forms. If so, ensure our process covers those forms if they need separate handling. Generally, if IRS is fine, states accept that 8879 covers it, but some have own forms (e.g., California FTB 8453-OL).
- **Legal Validity:** The e-signature must also meet general electronic signature laws (ESIGN, UETA) so it's enforceable if ever challenged. Using a reputable e-sign service or properly designed solution will ensure that.

By meeting these compliance points, we protect both our firm users and their clients, ensuring that an electronically signed 8879 via our software is fully acceptable to the IRS just as a pen-and-paper signature would be, and reduce any legal risk.

### 10.3 Client Authentication and Audit Trail for Signatures

**Requirement:** Implement strong client authentication for signing and maintain a detailed audit trail of the signature process.

- **Client Authentication for Portal/Signing:**

  - If client uses the portal with username/password, that itself is a form of authentication. But for signature, the IRS wants additional verification (the KBA as discussed).
  - We should ensure the link emailed to sign is unique and secret. Often e-sign invites have an embedded token in URL. That link should not require login (for simplicity) but then trigger KBA or at least identity confirmation like last 4 of SSN input.
  - Option: Ask client to enter a portion of their info to confirm identity before showing the doc (some solutions do ask to enter e.g. last 4 SSN and zip code, something the actual person knows).
  - Multi-factor### 10.3 Client Authentication and Audit Trail for Signatures

**Requirement:** Verify the identity of signers and maintain a robust audit trail for each e-signature transaction.

- **Multi-Factor Authentication:** If using the client portal, require the client to log in with credentials to access documents. For email signing links, implement identity verification steps (e.g., the client must input a code sent to their phone or answer KBA questions before signing). This ensures the signer is indeed the taxpayer.
- **Knowledge-Based Authentication (KBA):** As noted, for remote e-signature of IRS forms, the system will utilize KBA for an added layer of ID verification. The signer will answer a few personal questions generated from public records (e.g., loan amounts, previous addresses) before they can apply their signature. A passing KBA result is logged.
- **Detailed Audit Log:** For each signature request, record every step: when the document was sent, when the client viewed it, what IP address and device were used, when they authenticated, and when they applied their signature. This log (often called a **Signing Certificate**) will be attached to the signed PDF or stored in our database. It typically includes a unique document hash to detect any tampering.
- **Tamper-Proof Documents:** After signing, the PDF should be locked to prevent edits. Any alteration would invalidate the built-in digital signature or hash. This preserves the integrity of the signed 8879 or other documents.
- **Preparer Oversight:** The preparer or firm admin can view the status of outstanding signature requests (e.g., “Sent – not yet signed,” “Viewed by client,” “Signed by spouse pending taxpayer”). They can also revoke or cancel a request if needed (which would void the link).
- **Retention:** The system will retain the signed documents and audit trails for at least the required period (IRS requires EROs to keep Form 8879 for three years). Even if the client portal account is deleted, the firm’s copy of the signed form stays archived for compliance.
- **Compliance Checks:** The audit trail and authentication measures together ensure our e-signature process meets IRS standards for electronic signatures in a remote transaction – including the KBA identity proofing requirement. This protects the firm in case of IRS scrutiny or if a client ever disputes a signature.

### 10.4 Document Storage and Retrieval

**Requirement:** All electronically signed documents must be securely stored and easily retrievable when needed.

- Once signed, the finalized PDF (e.g., signed Form 8879) is automatically saved in the client’s document folder in the software. Preparers can download or print it at any time.
- The document storage is encrypted and access-controlled. Only users from the firm with proper permission can view the signed forms. Clients can be given a copy through the portal, but they cannot delete or alter the stored version.
- The system should tag or label documents as “Signed” vs “Unsigned” so it’s clear which version is final. The unsigned request PDFs can be discarded or kept separately once signing is complete.
- In the client’s profile, a section like “Authorizations” can list the status of Form 8879 (e.g., “Signed on 3/10/2025 by John Doe”) and provide a one-click open of the signed form. The preparer can also upload a manually signed document’s scan if they chose to get wet signature, to keep records in one place.
- During an IRS audit of the preparer, the firm should be able to produce any signed authorizations quickly. The software should allow exporting selected documents (with their audit logs) for compliance reviews.
- If the firm uses the e-sign system for engagement letters or other non-IRS forms, those too are stored similarly for full recordkeeping within the client’s file.

Integrating e-signature tightly into the workflow speeds up turnaround and maintains compliance. By covering secure authentication, proper logging, and easy retrieval, the software ensures that **electronic signatures are captured in a legally and IRS-compliant manner**, meeting the need for integrated e-sign functionality.

---

## 11. Tax Planning and Reporting

Beyond compliance and filing, professional tax preparers often provide tax planning advice and need to analyze tax data. The software will include features for tax planning and for generating various reports.

### 11.1 Tax Planning Tools (What-If Scenarios and Projections)

**Requirement:** Enable preparers to run projections and “what-if” scenarios using client data to assist in tax planning for future years.

- **Scenario Analysis:** The software should allow the creation of alternate scenarios based on a client’s current return or from scratch. For example, duplicating the current return data into a “What-if Scenario 1” where the preparer can change certain inputs (income, filing status, contributions, etc.) to see how the tax outcome would change. This does not affect the actual filed return – it’s a sandbox for planning.
- **Multi-Year Projections:** Provide a tool to project a client’s tax over multiple years. For instance, if in the current year the client had an exceptional capital gain, how will next year look if that is removed? Or project retirement scenarios: show this year vs five years later when client retires with different income streams. Possibly implement a simple engine for next year’s calculation (with expected inflation adjustments).
- **Planning for Estimated Taxes:** Use the current return data to generate estimated tax calculations for the coming year. Allow adjusting income assumptions for each quarter. The software can then produce estimated tax payment vouchers (Form 1040-ES or state equivalents) for the client. This ties planning with compliance, ensuring clients don’t underpay during the year.
- **Optimization Suggestions:** The software could highlight strategies, such as “Contributing an extra \$X to a Traditional IRA could save \$Y in taxes” if the scenario analysis shows a benefit. Or “If you buy equipment and take Section 179, your business tax drops to Z.” These suggestions might be automated in future enhancements, but at least the tools to test those strategies should be present.
- **Carryover Planner:** A feature to show how using or not using carryovers affects future years. E.g., if a client has a large NOL, how many years will it take to fully use it under current income assumptions? Or if they can defer some income to next year, how much of the NOL will remain?
- **Interface:** Possibly a separate “Tax Planner” module or mode. Data from the actual return can be imported into the planner with one click, then modified. The planner should clearly label outputs as hypothetical. It should not accidentally get filed – separate from the preparation workflow.
- **Save Plans:** Allow saving multiple named plans for a client (e.g., “Retire at 62 scenario” vs “Retire at 65 scenario”) and printing a comparative report. This adds value for the preparer’s consultation services.
- **Limitations:** Planning calculations should use current law by default, but perhaps allow toggling known future law changes (e.g., if tax cuts are set to expire in 2026, a planner might simulate that).
- These planning features help preparers offer proactive advice, aligning with how some professional software **“support tax planning features that help preparers offer proactive tax advice”** as a value-add beyond basic filing.

### 11.2 Historical Data Analysis and Year-over-Year Comparison

**Requirement:** Provide reports and views that leverage historical tax data for analysis and client communication.

- **Year-over-Year Comparison:** The software can generate a report comparing this year’s return to last year’s for the same client. Show side by side: prior year vs current year for key figures (income, deductions, credits, tax, refund). Highlight significant changes or variances beyond a threshold. This helps in review and also in discussing with the client why their tax might have changed (e.g., “Your wages increased by 15%, which raised your tax by X%”).
- **Multi-Year Summary:** For long-time clients, generate a summary of, say, the last 3-5 years of key data (AGI, taxable income, tax liability, effective tax rate, etc.). Perhaps present this in a chart or table. This can help identify trends (like steadily rising income) and inform planning (like gradually increasing estimated payments).
- **Effective Tax Rate and Other Metrics:** Calculate and report the client’s effective tax rate, marginal tax bracket, etc., and compare year-over-year. These metrics are often of interest to clients and preparers to evaluate tax efficiency.
- **Audit Flags Review:** Use historical data to spot anomalies – for example, if charity donations jumped unusually, it might catch IRS attention; the software can flag that in a review report. (This overlaps with compliance but using history as context).
- **Industry Benchmarks (for business returns):** If possible, provide some benchmark comparison for business clients. For instance, compare a client’s expense ratios to industry averages (this may be a future enhancement requiring data sources). At least, the software could allow exporting data to Excel for the preparer to do such analysis.
- **Visualization:** Include simple graphs in reports for clients – e.g., a bar chart of tax liability over five years, or a pie chart of what categories contributed to their taxable income. Visual aids can be part of a deliverable the preparer gives to clients in an annual review meeting.
- **Data Mining (For firm’s internal use):** The software could let the firm aggregate anonymized historical data across clients to find insights (like average refund amount, or how many clients have high medical expenses etc.). This is more practice management, but the data is there. Not a core requirement, but potentially a reporting feature for the firm’s strategy (e.g., identify clients who might benefit from a new tax law change).
- Essentially, these features turn raw tax return data into useful information and narratives, enhancing the preparer’s advisory role.

### 11.3 Client Tax Reports and Summaries

**Requirement:** Generate clear, client-friendly reports that summarize tax information, beyond the standard government forms.

- **Tax Summary Letter:** The software can create a summary letter to the client explaining the results of their return in plain language. For example: “Dear Client, your 2024 taxable income is \$X, and your total tax is \$Y. After \$Z of withholding, you have a refund of \$W.” Include a brief explanation of any major items (like “We included a \$ABC deduction for your mortgage interest, which saved you \$DEF in federal tax.”).
- **Payment Vouchers and Instructions:** If the client has a balance due, generate a payment voucher (or instruct how to pay electronically) with amount and due date. If they have estimated payments for next year, produce a schedule and vouchers for those. Similarly for state taxes.
- **Tax Planning Recommendations:** A report that lists suggested actions (entered by preparer or possibly auto-generated) for future tax savings. For instance, “Recommendation: Increase 401(k) contributions to reduce next year’s tax” or “Consider quarterly estimated payments of \$X to avoid underpayment penalties.” The preparer can customize this and include it with the client’s copy.
- **Supporting Schedules for Client:** Some clients like to see detailed breakdowns (e.g., a worksheet of how we arrived at taxable Social Security amount). The software could produce supplemental schedules (not just official forms) that show calculations clearly. This is useful for transparency and if the client is ever questioned.
- **K-1 Packages:** For business returns, when K-1s are generated for partners/shareholders, the software can produce a cover letter or explanation for each recipient along with their K-1, possibly including pointers on where to report those K-1 items on their personal return. This makes it easier for the recipients (and is a service the firm can provide).
- **Presentation and Format:** All reports should be well-formatted, possibly with the firm’s branding (logo, header). Allow exporting to PDF or Word so preparers can tweak wording if needed.
- **Summary for Bank/Loans:** Sometimes clients need a quick summary of income for loan applications. The software could generate a basic income verification report (basically re-stating AGI, taxable income, etc., with the firm’s sign-off). Not a tax requirement, but a useful extra.

### 11.4 Firm-Level Reports (Practice Management)

**Requirement:** Provide reporting tools for firm users to analyze and monitor their tax practice using the software’s data.

- **Productivity Reports:** For example, number of returns prepared per preparer, average time to complete (if time tracked), how many returns are in each status (in progress, waiting for client, filed, etc.). This helps managers identify bottlenecks.
- **E-File Volume Report:** Count of e-filed returns by type (1040, 1120, etc.) and their acceptance rates. Useful for firm to reconcile with IRS e-file acknowledgments and for performance metrics (and perhaps for software pricing if based on volume).
- **Revenue Reports:** If the software tracks fees or invoices (perhaps through the payment handling module), it can report total fees earned per client or in aggregate, which clients are most profitable, etc. Even if it doesn’t handle billing fully, the preparer could input the fee charged for each return and then generate a report (e.g., total billings this tax season).
- **Extension Lists:** A report listing all clients on extension and their status (filed or not). Good for off-season planning.
- **Due Date Calendar:** A calendar view or report of upcoming filing deadlines, including business fiscal year-ends, extension deadlines, etc., across the client base.
- **Client List Export:** Ability to export a list of all clients with basic data (for mailing lists or marketing – e.g., to send a newsletter).
- **Data Mining Queries:** Possibly allow custom queries, like “show all clients who have Schedule C with income over \$X” (which could be used to market additional services to those clients). This may be advanced, but a simpler approach is export to Excel and let the user filter.

These practice-oriented reports turn the software into not just a compliance tool but a management tool for the firm. While not all are critical to initial release, including a few key reports (year-over-year comparisons for clients, status dashboards, etc.) will greatly enhance the user experience and are expected by product managers in a full-featured system.

---

## 12. Payment and Fee Handling

Professional tax preparers need to collect their fees, and sometimes facilitate payment of taxes or distribution of refunds. The software will include features to handle these financial aspects.

### 12.1 Invoicing and Direct Payment Collection

**Requirement:** Allow the firm to calculate fees and collect payment directly from clients through the software.

- **Fee Calculation:** The firm admin should be able to set up billing rules (e.g., flat fee per return type or per form, or hourly rates, or per complexity). While comprehensive billing is beyond scope, at minimum the software could allow entering a fee amount for the engagement.
- **Invoice Generation:** Create a simple invoice or billing summary for the client. It would list services (e.g., “Tax preparation for 2024 tax year”) and amount due. This can be printed or sent via the client portal/email.
- **Integrated Payment Gateway:** The software should integrate with a payment processor (Stripe, PayPal, etc.) so that clients can pay their tax prep fees online. For instance, an invoice email or portal page could have a “Pay Now” button. The client can enter credit card or ACH info and make a payment.
- **Recording Payments:** When a payment is made, mark the client’s invoice as paid in the system and possibly note the method/date. If partial payments are allowed, track balance due.
- **Multi-Currency/Locale:** Probably not needed since it’s US taxes, fees will be USD.
- **Security for Payments:** Ensure PCI compliance by using hosted payment fields or tokenization (so our system never stores full card info). The payment gateway handles the secure part.
- **Notification:** Notify the preparer/admin when a payment is made. Possibly have a dashboard of who has paid vs who hasn’t (so they can chase unpaid fees).
- **Reporting:** Summarize fees collected over period, to help firm accounting.
- **Optional Use:** Not all firms will use this if they have external billing, so it should be optional. The system should function if the firm chooses to bill outside. But having it integrated is a convenience that many will appreciate, as it centralizes tax workflow and payment.

### 12.2 Fee Deduction from Tax Refund (Integration with Bank Products)

**Requirement:** Support the option for the preparer’s fee to be deducted from the client’s tax refund, using third-party refund transfer programs (bank products).

- **Refund Transfer (RT) Integration:** Partner with bank product providers (e.g., Santa Barbara TPG, Republic Bank, Refundo, etc.) that offer “refund transfer” or “refund settlement” services. In this model, the bank sets up a temporary account to receive the client’s IRS refund, subtracts the preparer’s fee (and any bank fee), then sends the remainder to the client (via direct deposit, check, or prepaid card).
- **Workflow in Software:** If the client opts for this:

  - The preparer checks a box “Deduct fee from refund (Bank Product)”.
  - The software collects additional info required by the bank: client bank details for final deposit, consent forms, selection of disbursement method (check, direct deposit, etc.), and identity info to comply with banking KYC (possibly SSN, DL number if not already).
  - The software generates the bank product application forms. These can often be e-signed along with the 8879 since they’re part of the tax package.
  - The e-file transmitted to IRS will use the bank’s routing and account number for the refund deposit. The software should automatically plug those in when bank product is chosen, instead of the client’s own bank. This is critical – it directs IRS to send refund to the intermediary bank.

- **Fee Setting:** The software communicates the preparer’s fee amount to the bank so that amount is withheld. Possibly also allows adding a bank service charge. These details are usually embedded in the bank application data.
- **Real-time Acknowledgment from Bank:** Once IRS accepts the e-file, the bank partner system will notify when the refund is received and when the funds are released to client and fee to preparer. The software should integrate with the bank’s API or portal to get status updates (e.g., “Refund disbursed on March 1, fee deposited to your account.”). At minimum, provide a link for the preparer to check status on the bank’s site, but ideally within our interface show statuses.
- **Security/Privacy:** Treat this financial data carefully. It’s essentially like a mini financial transaction system within our software. All data transmitted to the bank must be encrypted. The client’s consent is required for these programs (the software should capture a signed consent form like 7216 consent if needed for disclosing tax info to bank).
- **Support Multiple Banks:** Some firms use different bank product vendors. If feasible, integrate with a few popular ones and allow the firm to choose a preferred provider in settings. This could influence the forms and process slightly (each bank has its own enrollment and fee structure).
- **Bank Enrollment for Firm:** Typically, a firm must enroll with the bank product provider at season start. The software can facilitate this by either guiding them to sign up or possibly handling enrollment inside the software (like fill a form to enroll the EFIN with the bank).
- **Benefits:** By offering this feature, we address preparers who advertise “File now, pay fees out of your refund” – an attractive option for clients who can’t pay upfront. Many pro packages include this integration as a standard feature.

### 12.3 Refund Distribution and Tracking

**Requirement:** Provide options and tracking for how client tax refunds are handled, whether or not a fee deduction is involved.

- **Direct Deposit to Client:** If the client wants a direct deposit of their refund to their own account (most common), the software collects the routing and account number in the return input. This goes to the IRS e-file. The system should validate the format of these numbers to reduce errors (check digit validation for routing).
- **Split Refunds:** If the client wants to split the refund into multiple accounts or buy savings bonds (Form 8888 usage), support entering those details (account 1, amount or percentage, account 2, etc.). The software generates Form 8888 and includes it in e-file.
- **Paper Check:** If the client wants a paper check from IRS, just ensure no direct deposit info is entered and possibly the e-file indicates check. The software can note “Refund via check – mailed to address on return.”
- **Refund Status Tracking:** While the IRS has the “Where’s My Refund” tool, our software could integrate with IRS e-file status updates for refunds if available (currently, IRS doesn’t provide API for refund status to software, but some bank product providers track it). At minimum, the software can store the date the refund was expected (IRS states 21 days for most e-filed refunds) and allow the preparer to record when client received it (if they inform).
- If using the Bank RT product, as mentioned, track through the bank’s system – often the bank effectively becomes the tracker (they’ll know when IRS funded the account).
- **Balance Due Handling:** If the client owed money instead of refund:

  - The software can facilitate payment. Options: electronic funds withdrawal (EFW) as part of e-file (client provides bank info and date to pull funds – we support that input). Or instruct the client to pay via IRS Direct Pay or check. We generate the payment voucher (Form 1040-V) if needed.
  - Track if client actually paid (maybe out of band – we likely rely on client to do it; the software can send reminders of payment deadline).

- **Notifications to Client:** Possibly the system can send the client an email when their refund is deposited (if using bank product integration, we get that info). Otherwise, the preparer might manually notify or the client checks IRS tool.
- **Fee Collection Tracking:** If not using refund deduction, ensure the preparer has marked the fee paid by some other means. See section 12.1 – those tie together: either the client pays up front (recorded in system) or via refund. No client should slip through without fee recorded (maybe a dashboard can show any returns filed where fee not marked paid and no refund deduction used, as a sanity check for firm’s accounts).

### 12.4 Payment Processing Security and Compliance

**Requirement:** Ensure that all features involving money (fee payments, refund transfers) are handled securely and in compliance with relevant regulations.

- **PCI Compliance:** For credit card processing of fees, do not store sensitive card data on our servers. Use tokenization or hosted fields from the payment gateway. Undergo PCI DSS SAQ if needed to verify compliance because we facilitate payments.
- **SSL/TLS:** All pages where payment info is entered by client (or bank info for refund) must be served over HTTPS with strong encryption.
- **Privacy of Bank Info:** The client’s bank account for direct deposit or debit is highly sensitive. Store it encrypted in the database (and perhaps not at all after filing – could be just in the XML and then removed, or retained if needed for amendment use, but encrypted and access-limited). Comply with IRS Publication 1075 if applicable for safeguarding personal info, and GLBA rules since it’s financial info.
- **Authorization and Consent:** Ensure the client explicitly consents to any direct debit of taxes due (on IRS Form 8878/8879 they usually sign for that as well if applicable). Similarly, if using refund transfer, the client signs a consent that outlines bank fees. The software should present these consents clearly.
- **Audit Logging:** Log any changes or views of sensitive payment data by firm users (e.g., if someone edits the direct deposit info, record user and time). This ties to audit trail (section 13).
- **Regulatory Compliance:** If operating in states with strict data laws (like California Consumer Privacy Act), ensure we allow deletion of payment data after use if requested, etc. For bank products, comply with banking regs (the partner bank will handle the actual compliance, but we must follow their program rules).
- **Separation of Duties:** Within the software, consider restricting who can initiate a bank product versus who can approve it (to prevent misuse). Possibly an admin must enable bank product feature and accept terms with the bank.
- **Updates:** Keep the integration updated with any new security measures from payment providers or bank partners (for example, if a bank moves to a new API or adds multi-factor for preparers logging into their portal).

These measures ensure that the convenience of integrated payments and refund handling does not introduce undue risk. Ultimately, the goal is to **make fee collection seamless (even via refund deduction) while keeping all transactions secure and compliant**.

---

## 13. Audit Trail and Logging

For a professional system dealing with sensitive financial data, a comprehensive audit trail is essential. It provides accountability, helps detect unauthorized changes, and is often needed for regulatory compliance.

### 13.1 Change Tracking (Who, What, When)

**Requirement:** Track every significant change to data in the system, recording what was changed, who made the change, and when.

- **Field-Level Tracking:** When a preparer edits a tax return field (e.g., changes income from 50,000 to 60,000), the system logs that “User Jane Doe changed Line 1 Wages from 50000 to 60000 on March 5, 2025, 14:30:22.” It may not be practical to log every single field due to volume, but at least log at form/subform level or key values. Critical fields like refund amount, bank account info, etc., definitely log.
- **Status Changes:** Log changes in status (like marking return as reviewed, or transmitted, or signed). E.g., “Return status changed to ‘E-file Transmitted’ by User John at 15:00:00.”
- **Uploads/Downloads:** Log when documents are uploaded or downloaded. E.g., “Client uploaded W-2.pdf” or “Preparer downloaded signed 8879.pdf on \[date].”
- **User Management Logs:** Log creation of new user accounts, role changes, password resets (admin initiated), login attempts (especially failures for security).
- **Configuration Changes:** If admin changes firm settings (like EFIN entered, or fee settings), log that.
- **Non-Editable Logs:** Ensure that once written, these logs cannot be altered or deleted by normal users (including admins). They may be stored in an append-only format or separate database. This prevents tampering to cover tracks.
- **Viewing Logs:** Provide authorized users (likely admins, or the firm principal) the ability to view the audit logs. Possibly filter by client or by user or date range to find relevant events. For security events, maybe only admins get full detail.
- **Performance Consideration:** Logging every action can produce a lot of data. We’ll optimize by focusing on substantive changes (not every keystroke, but final changes on field blur or save). Use a separate log storage table to not slow down normal operations.
- **Retention:** Keep audit logs for a certain period (perhaps indefinitely for tax changes, or at least as long as the client exists in system plus some years). Possibly archive older logs if needed.

### 13.2 Access Logs and Activity Monitoring

**Requirement:** Monitor and record user access to sensitive data, helping detect unauthorized access.

- **Login/Logout Tracking:** Every login (successful or failed) is logged with timestamp and source IP/device. Repeated failed logins could trigger alerts (potential attack or forgotten password scenario).
- **Session Timeout Logs:** If a user is auto-logged out after inactivity, note that too (for completeness).
- **Data Access:** If a user views a tax return or opens a client’s personal details page, log that “User X viewed Client Y’s tax return on \[date/time].” This might be needed especially in multi-user environment to audit that only authorized staff are accessing a client.
- **Exports/Prints:** If a user exports data (like a PDF of a return, or an Excel of client list), log that action, as it involves data potentially leaving the system.
- **Admin Views:** If an admin uses any impersonation feature (some systems let admin view things as another user for support), log that the admin accessed it.
- **Real-time Monitoring:** Possibly have an admin dashboard that shows currently logged-in users or recent activity, to monitor active usage.
- **Alerts for Unusual Activity:** If the system notices abnormal patterns (e.g., a user accessing an unusually large number of client records in short time, which might indicate data theft, or access at odd hours or from new location), it could alert the admin. This might be advanced but is part of security best practices.
- **Client Access Log:** Even clients could have their access logged (e.g., client viewed their tax summary on portal).
- **Privacy Consideration:** These logs are internal for security; ensure only appropriate oversight roles can see them (we wouldn’t want one preparer to see logs of another preparer’s activity, generally).

### 13.3 Audit Trail for Compliance and Reviews

**Requirement:** Utilize the audit trail information to support compliance requirements and internal review processes.

- **Regulatory Compliance:** If the firm is subject to a security audit (like SOC 2 or IRS Safeguards), the audit logs demonstrate controls. The software should allow export of logs needed for auditors (perhaps filtering to specific events). E.g., show a regulator all access to PII in the last year.
- **Internal QA and Peer Review:** If a return had an issue, the firm can review the logs to see who entered a particular figure or who approved it. This accountability can inform training (e.g., if one team member frequently has changes after review, maybe more training needed).
- **Protect Against Fraud:** Sadly, there are cases of internal fraud (e.g., someone altering returns to divert refunds). The audit trail would capture any such alterations. For instance, if a bank account for direct deposit was changed, the log shows who did it. This can deter malicious behavior and also be evidence if needed.
- **Client Transparency (if needed):** In rare cases, a firm might even share a portion of the log with a client to explain what happened (e.g., “Our records show you authorized this change on this date”). Not typical, but the data is there if ever needed legally.
- **Edit/Amend History:** The audit trail can serve as a de-facto “version history” of the tax return. Some software present a diff of before/after if an amendment is done. We could use the logs to reconstruct what changed from original to amended. Perhaps not user-facing, but it’s there to be mined if needed.
- **Archiving Logs with Return:** When a return is finalized (filed), it might be useful to snapshot certain logs with it. For example, store a summary of who prepared and who reviewed and when, with the return archive. So even if logs database is purged years later, that key info stays attached to the return record.

### 13.4 Reporting and Export of Audit Logs

**Requirement:** Provide means to report on and export audit trail information for analysis or compliance reporting.

- **Audit Reports:** Pre-built reports like “User Activity Report” (show everything a particular user did in a timeframe) or “Client Change History” (all changes for a specific client’s data). This saves manual filtering.
- **Export Function:** Allow an admin to export audit logs to CSV/Excel for external analysis or long-term archiving. They might use this if migrating to another system or for an investigation requiring log analysis with tools.
- **Log Integrity:** When exporting, include a hash or digital signature of the log data to prove it’s unaltered, if presenting as evidence.
- **Volume Management:** If logs are huge, allow exporting by segments (e.g., one month at a time) to manage file sizes.
- **Integration with SIEM:** Larger firms might have a Security Information and Event Management system. If so, our software could output logs in a format that can be ingested by such systems (like JSON or a syslog stream). This is advanced and likely optional, but our design could foresee an API to fetch logs.
- **Privacy in Logs:** Ensure logs themselves don’t expose sensitive data unnecessarily. For example, avoid printing full SSN or account numbers in logs; better to reference “client X’s account changed” without including the entire number. Use unique client IDs rather than names in back-end logs if worry of PII. Or mask parts of data in logs (e.g., show last4 of SSN).
- **Time Synchronization:** All logs should use a consistent timestamp (ideally UTC stored, display in local). Sync server clocks to avoid mismatches (especially important if multi-server).
- **Retention Settings:** Possibly allow the firm to set how long to retain logs if storage is a concern (but default to at least several years). For compliance, longer is better, but maybe configurable.

In summary, a robust audit trail subsystem underpins the trust and accountability in the software. It helps fulfill regulatory responsibilities and gives the firm oversight over the actions taken in the system – a must for any sensitive financial application.

---

## 14. Integration with External Systems

(_Note: Many integration points have been covered in Section 9 and Section 10 (for e-signature) and Section 12 (for payments). This section summarizes external integration capabilities and ensures no major integration need is overlooked._)

### 14.1 Accounting Software and Financial Data

As detailed in **Section 9.1**, the software integrates with accounting systems like QuickBooks to import financial data, and can ingest files (CSV, Excel) from other bookkeeping systems. This eliminates re-keying of financial statements by pulling trial balances and transactional data directly. The system’s open API (Section 9.4) further allows custom integrations with any financial software if needed.

### 14.2 Banking and Payment Gateways

The software connects to payment processors (Stripe/PayPal, etc.) for collecting preparation fees via credit card (Section 12.1) and to refund transfer partner banks for fee deduction services (Section 12.2). These integrations involve secure data exchange with financial institutions, adhering to industry standards for encryption and data security. Through these, the product extends its functionality into the financial domain, letting preparers manage billing and refunds within one system.

### 14.3 Third-Party Services (Payroll, Document Management, etc.)

Beyond accounting data, the software can import data from payroll providers (W-2s from ADP, etc.) and brokerage firms (1099-B, 1099-INT, -DIV via file import), as described in **Section 9.3**. If the firm uses an external document management system or cloud storage (like Dropbox, Google Drive), future integration could allow importing client documents from there or exporting copies of returns. While not in initial scope, the architecture’s API framework makes such additions feasible.

### 14.4 Open API for Custom Integrations

We provide a **REST API** (perhaps in a later release) for firms or third-party developers to integrate the tax software with other tools (CRM, practice management, etc.). With appropriate authentication, they can perform tasks like creating clients, pulling status updates, or pushing data. For example, a practice management system could use the API to fetch which clients’ returns are completed versus pending and display that in a central dashboard. This openness ensures the software can fit into a firm’s broader software ecosystem, which is important for larger practices that rely on multiple specialized systems.

**Summary:** The professional tax software is not a silo; it’s built to connect with other systems to streamline the preparer’s workflow. From importing data to exporting results and handling e-sign and payments via third parties, integration capabilities are woven throughout the requirements. This integrated approach reflects the reality that tax prep intersects with accounting, finance, and document management systems in a modern office.

---

## 15. Deployment and Hosting Options

The product will be offered in flexible deployment models to cater to different firm preferences: as a cloud-based SaaS and as an on-premise solution. Each option has its requirements and considerations, outlined below.

### 15.1 Cloud (SaaS) Deployment

**Overview:** In the cloud deployment, the software is hosted on secure servers managed by us (the vendor) and accessed by users via web browser (and possibly desktop app interface or mobile). Most modern professional tax solutions are moving to the cloud for ease of access and maintenance.

**Key Requirements and Features:**

- **Multi-Tenancy:** The SaaS environment will be multi-tenant – meaning multiple firms (tenants) use the same application instance with logical data isolation. Each firm’s data is segregated and protected from others’. Unique firm IDs or separate databases ensure no commingling of data.
- **Scalability:** The cloud system must scale to handle many users across many firms, especially during peak filing season (see scalability in Section 16.1). This likely involves load balancers, multiple application servers, and auto-scaling infrastructure (e.g., using cloud services like AWS, Azure, or GCP).
- **Automatic Updates:** One major advantage – all users get updates automatically. When a new tax law update or patch is released, it’s applied on the server side, and next login everyone has the latest version. This simplifies the annual rollout and mid-season fixes.
- **Accessibility:** Users can log in from anywhere with internet, which supports remote work and multi-office firms. The system should be optimized for performance over typical broadband connections, and possibly usable on tablets for on-the-go access.
- **Data Backups:** The hosting should include regular backups of all client data. Ideally daily incremental backups and the ability to restore data in case of any corruption or user error (e.g., if a user accidentally deletes a client, admin can request a restore from backup).
- **Security Measures:** Cloud deployment means we (vendor) are responsible for infrastructure security. This includes firewalls, intrusion detection, routine security audits. Data at rest in the cloud database is encrypted. Strong user authentication (with optional 2FA) is implemented to prevent unauthorized access from the internet.
- **Compliance (SOC 2, etc.):** Many firms will require that our SaaS environment meets industry security standards (SOC 2 Type II certification, etc.). We should design and operate the cloud with those best practices (access controls, logging, disaster recovery, etc., many covered in Section 16).
- **High Availability:** The service should target a high uptime (e.g., 99.9% or better during Jan-Apr) – see Section 16.4. We may deploy in multiple data centers (or cloud regions) for redundancy.
- **Support and SLAs:** Provide a Service Level Agreement for firms that outlines uptime commitments and support response times. Also have capacity for increased support during peak times for the cloud service.

In summary, the SaaS deployment offers convenience and centralization. Product managers should ensure that the user experience in the cloud is as responsive as a desktop and that firms trust the cloud with their sensitive data – hence heavy emphasis on security and reliability.

### 15.2 On-Premise Deployment

**Overview:** Some firms (especially larger or those with strict IT policies) may prefer an on-premise deployment. This means the software can be installed on the firm’s own servers (or private cloud) and run locally, with data stored on-premise under their control.

**Key Requirements and Features:**

- **System Requirements:** We will provide specifications for servers (OS support, hardware requirements). Often, on-prem might be a Windows Server (since many tax software historically Windows-based) or could be provided as a virtual appliance or Docker container for easier deployment. We need to support common environments (Windows/Linux servers, with required runtime like application server and database).
- **Installation and Updates:** There must be an installer or deployment package. The installation should set up the application, databases, etc., with minimal hassle. Yearly updates would require the firm to install a new version or apply patches. We should make this process as smooth as possible (perhaps an in-app update mechanism or at least clear documentation).
- **Data Migration:** Ability to import data from one version to the next (carryforward of data across versions) needs to be handled locally – possibly via a migration utility. If a firm switches from SaaS to on-prem or vice versa, provide export/import paths (maybe an export of all client returns to an encrypted file that can be imported).
- **User Management:** The firm’s admin would manage user accounts in the application. Optionally, integrate with the firm’s Active Directory/LDAP for single sign-on (so employees can log in with their usual network credentials). This might be an advanced feature but is often requested by enterprise clients.
- **E-File Setup:** On-prem servers need internet access for e-filing. We must ensure the application can connect to IRS and state servers from the firm’s environment. If their network has proxies or firewalls, provide configuration to accommodate that. Also, ensure that any required IRS communication certificates or protocols are correctly configured on-prem.
- **Security:** The firm’s IT will handle perimeter security, but our software should still enforce application-level security (authentication, encryption of data at rest, etc.). Possibly provide guidelines to the firm (like “use SSL for the web app”, “configure a firewall to only allow necessary ports”). Data resides on their servers, so encryption of sensitive fields in the database (like passwords, SSNs) is still our responsibility in design.
- **Support for Multi-Office:** On-prem installation could be single server or distributed (app server + DB server separate). For performance, a large firm might deploy the database on a beefy SQL Server and multiple app instances across offices. The software should allow that (maybe a config for DB connection so multiple app nodes connect to one DB).
- **Maintenance:** The firm will be responsible for backing up their database. We should supply tools or instructions for backup (perhaps a scheduled backup feature built-in, or at least document the DB backup procedures). Also, if any maintenance tasks (like re-indexing database, clearing temp files), document those.
- **Feature Parity:** Ensure the on-prem version has all the same features (e-sign, integrations, etc.) or note if any feature is cloud-only. For example, some cloud-specific features (like using our hosted payment service) should also work on-prem, meaning the on-prem server still calls out to payment gateway directly. If something truly requires cloud (like a machine learning service or big data analysis), consider delivering it as an optional connected service or making it self-contained. Ideally, avoid feature disparity so on-prem users don’t feel second-class.
- **Licensing and Updates Control:** The on-prem version might use a licensing system (perhaps a license key tied to number of users or returns). The app could enforce license limits. Also, the firm might delay updates if needed – but emphasize that tax law updates should be applied or e-filing might not be allowed (IRS will reject outdated formats). Possibly disable e-file if software is not updated beyond a certain date to ensure compliance (with notifications in advance).

On-prem deployment offers control and possibly performance benefits (if internal network is faster and no internet dependency for usage). However, the firm assumes responsibility for infrastructure. Product managers should weigh the maintenance overhead, but offering on-prem expands market to those who cannot use cloud for policy or connectivity reasons.

### 15.3 Hybrid Considerations

**Requirement:** Address any use of both deployment models or migration between them.

- A firm might start on SaaS and later move on-prem (or vice versa). We should plan for data migration between cloud and on-prem. That might involve an export of all data (perhaps an encrypted backup provided to them) and an import utility in the on-prem installation to load it, preserving all client files, carryovers, etc.
- Some large organizations might want a private cloud hosted by us – essentially an on-prem but we manage a dedicated instance for them (common for enterprises that want data isolation but don’t want to maintain it themselves). While not explicitly required, our architecture should allow single-tenant dedicated deployments if needed (maybe via a separate environment).
- Ensure that features like e-signature and bank integration, which rely on cloud services, are accessible to on-prem. For e.g., an on-prem server might call DocuSign API directly (needs internet) or route through our cloud. Likely it will call directly out to those third parties.
- If offering a hybrid (some data on-prem, some in cloud), likely not necessary. Simpler to choose one or the other per firm. But we might update on-prem from cloud (like license updates or form updates could be downloaded from our servers automatically).
- For support, the hybrid might mean our support staff sometimes needs to access an on-prem system for troubleshooting. That can be tricky; maybe collect logs or have a remote support tool.

### 15.4 Multi-Tenancy and Data Isolation

_(Primarily relevant to Cloud deployment, but also to multi-client handling on-prem)_

**Requirement:** Ensure that each firm’s data is isolated and secure from others, and design multi-tenant data structures accordingly.

- In the cloud database, include a firm/org identifier on all relevant tables to partition data. All queries in the app must be filtered by the current firm context, to prevent any data leakage across firms.
- Use access control at the application layer such that users can only see data belonging to their firm. Even if multi-tenancy, one firm’s user should never be able to query another firm’s info.
- Consider using separate schema or separate database per tenant if needed for extra isolation (at cost of overhead). Or a hybrid: one DB but very strong ORM tenant enforcement.
- During deployment and testing, use sample multi-tenant scenarios to verify no cross-tenant data appears (a critical security test).
- For on-prem, multi-tenancy is not about multiple firms, but rather multiple users within the firm. Data isolation is then about role-based access (Section 3) where perhaps certain users only see certain clients if configured. Ensure those internal permissions are applied consistently in queries and UI.
- Data encryption keys or secrets should be tenant-specific if possible (so even in the unlikely event of cross-tenant access, encrypted fields from another tenant wouldn’t be decipherable).
- Backups and exports in cloud should be tenant-scoped – e.g., if a firm requests their data export, we only give theirs.
- **Testing and Staging:** In our cloud environment, maintain separate staging environments for testing updates to not impact all tenants at once. Roll out updates in a controlled way (maybe pilot with some tenants before all).
- **Performance Segregation:** Ensure one tenant heavy usage doesn’t starve others (e.g., one firm uploading massive data or running a huge report). This may require multi-threading and resource quotas or just robust infrastructure scaling.

In sum, the deployment flexibility is a selling point: **cloud for ease and on-premise for control**, with both given full support. Product management must plan for the development, testing, and support of two distribution methods, which is more work but opens the product to a wider user base.

---

## 16. Non-Functional Requirements

In addition to the rich set of features described, the software must meet several non-functional requirements that ensure it is fast, secure, reliable, and scalable. These qualities are crucial for user satisfaction and for meeting professional standards. Below we outline the key non-functional requirements.

### 16.1 Performance and Scalability

- **High Performance:** The application should be responsive under heavy usage. Typical operations (saving a return, running a calculation, generating a PDF) should take no more than a couple of seconds. Navigating between form sections should feel instantaneous (sub-1 second if possible), thanks to efficient front-end design and back-end queries.
- **Peak Load Handling:** The system must handle the surge of activity around tax deadlines (e.g., in the days leading up to April 15). It should support many concurrent users and transactions without slow-down. For example, if 1,000 preparers simultaneously calculate returns or transmit e-files, the system should handle that load.
- **Scalability:** The architecture will be **horizontally scalable** – we can add more server instances to handle more users. For cloud, auto-scaling triggers on CPU/memory usage will be in place. For on-prem, documentation will suggest hardware sizing based on number of users/returns (e.g., up to 20 users on a 8-core server, etc.).
- **Database Performance:** Use indexing and query optimization for the database so that retrieval of client records or searching thousands of returns is quick. Large firms may have tens of thousands of clients in the database – queries like global search by name or generating aggregate reports should still execute in seconds.
- **Throughput for E-filing:** The system should be capable of transmitting and processing acknowledgments for large batches of returns (say a firm files 500 returns in one go) within a reasonable time (a few minutes). Queuing mechanisms will manage throughput to IRS if needed while keeping the UI updated.
- **Client-Side Performance:** The web interface (if applicable) should load within a few seconds even on moderately fast internet. Use code-splitting to load heavy components (like forms library) only when needed. Minimize large downloads.
- **Resource Usage:** The application should be efficient in memory and CPU usage, to reduce cost in cloud and allow on-prem to run on standard hardware. Avoid memory leaks (especially in a long-running server process).
- **Testing:** Conduct load testing and stress testing prior to release. E.g., simulate peak hour with X thousand concurrent users adding forms, ensure response times stay within targets. Identify bottlenecks (maybe a particular report or query) and optimize or put limits (like heavy reports run off-peak).
- **Graceful Degradation:** If the system is under extreme load, it should still remain operational (maybe slightly slower but not crashing). Perhaps queue non-critical tasks or degrade certain features (like turn off real-time suggestions) to preserve core functionality.
- **Concurrent Editing:** If multiple users edit the same return (rare scenario), define behavior (either lock the return for one user at a time or merge changes carefully). Probably lock per return to avoid complex merge issues, and inform others that it's in use.
- **Scalability for Future Growth:** The design should accommodate growth in user base and data for years. If we onboard many more firms or if tax data grows (e.g., more forms, more years stored), the system can scale out with additional servers or partitioning data as needed.

### 16.2 Security and Data Privacy

- **Data Encryption:** All sensitive data (SSNs, EINs, account numbers, etc.) in the database will be encrypted at rest (using strong encryption like AES-256). In transit, all communication between client and server (or server-to-server) will be over encrypted channels (HTTPS with TLS 1.2+).
- **Authentication and Access Control:** Users must authenticate with a username/password (or SSO integration for on-prem option). Encourage strong passwords by policy (min length, complexity). Support **multi-factor authentication (2FA)** for users – especially admins – to add an extra layer (e.g., TOTP app or SMS code).
- **Role-Based Access:** As described in Section 3, fine-grained access ensures users only see and do what their role permits. Enforce these checks in the back-end for every request (never rely solely on front-end to hide things).
- **Account Lockout and Recovery:** Implement lockout after a number of failed login attempts to deter brute force. Provide secure password reset procedures (e.g., email reset link with verification, or admin can reset password for a user). Possibly incorporate security questions or other verification for resets if needed.
- **Activity Monitoring:** As per Section 13, extensive logging of user actions helps detect and investigate any suspicious activity. Potentially add real-time alerts for certain events (like admin gets an alert if a new admin user is created, or if a large export of data occurs).
- **Protection Against Common Vulnerabilities:** Follow OWASP best practices to prevent SQL injection, cross-site scripting (XSS), CSRF, etc. Use parameterized queries, encode outputs, require CSRF tokens on forms, etc. Perform security testing or audits (possibly hire an external firm to do penetration testing before release, given the sensitivity of tax data).
- **Isolation:** In the cloud, multi-tenant data isolation is critical (Section 15.4). Also ensure each user session is properly isolated (no session data bleed, use secure session cookies, etc.).
- **Data Privacy Compliance:** Adhere to privacy laws like GDPR (if any EU data, though product is US-focused, but could apply if US firm has EU resident data) and CCPA for California. This includes handling any client data deletion requests, etc. Ensure the privacy policy covers how data is used (we don't use client tax data for anything other than providing service, etc.).
- **IRS Safeguards Rule:** The IRS requires tax pros to have a data security plan and use tools that safeguard taxpayer data. Our software will be an ally in that by providing encryption, access logs, and 2FA, helping firms fulfill their obligations under regulations like the FTC Safeguards Rule.
- **Secure Development Process:** Adopt secure coding guidelines internally. Possibly obtain certifications like SOC 2, which will examine our security controls. Also, ensure any third-party libraries we use are up-to-date and without known vulnerabilities.
- **Disaster Recovery (Security aspect):** Maintain secure off-site backups (encrypted) in case primary data is lost, so it can be restored without data breach risk.
- **User Security Features:** Optionally allow admin to enforce periodic password changes, or to immediately disable a user account (if an employee leaves). Possibly allow IP whitelisting for on-prem or additional restrictions if desired by firm.
- **No Unnecessary Data Storage:** Only store data that’s needed. For example, if we don't need full credit card numbers, we never store them. If SSNs are not needed after e-file (they are, but hypothetically), we would purge or mask them. Minimize retention of PII beyond necessity.

### 16.3 Regulatory Compliance

- **IRS E-File Standards:** The software itself must comply with IRS requirements for software developers and transmitters. This includes passing the annual IRS Assurance Testing System (ATS) for all supported forms, using the correct electronic file formats and protocols. We will maintain our IRS certification each year and adjust to any new specs (e.g., if IRS updates schemas or adds new validation rules, our updates incorporate those).
- **Authorized E-File Provider Compliance:** The software should facilitate the firm’s compliance with IRS rules. For instance, IRS Pub 1345 details ERO responsibilities – our logs and e-sign process support that (keeping 8879, verifying identity, etc.). We might include checklists or reminders in the software to meet those (like a reminder to get Form 8879 signed before transmitting).
- **State Compliance:** Ensure compliance with state e-file programs and any state-specific regulations. Some states require additional registration of software – we will handle that on our side but ensure the software meets those technical requirements (like including state-specific data or forms).
- **Tax Law Compliance:** Functionally, the software must be updated for new tax laws (as discussed). Non-functionally, this is a commitment to release timely updates whenever laws change. E.g., if Congress passes last-minute tax changes in December, we will push an update ideally before filing season or as soon as possible. A process is in place to monitor tax law changes (federal and state) continuously.
- **Data Protection Regulations:** As touched in security, comply with laws like GDPR/CCPA if applicable. For example, if a taxpayer data falls under GDPR (maybe an expat’s info), the firm might ask for an export or deletion – the software should allow the firm to extract or delete data to comply (bearing in mind tax records usually are kept by law, so normally deletion is not required for at least some years).
- **Accessibility Compliance:** (Often overlooked, but a non-functional aspect) – Ensure the application meets accessibility standards (like WCAG 2.1 AA) so that users with disabilities (e.g., vision impairment using screen readers) can use it. This might be a requirement for government or larger institution clients. Not explicitly asked, but as a professional product, at least partially addressing it is good practice.
- **Audit and Verification:** If any external audits are required (like a SOC 2 audit, or IRS inspection for software providers), the team will maintain documentation and logs to demonstrate compliance. E.g., cryptographic protocols used, security policies, etc.
- **Regulatory Changes in Software Industry:** Keep an eye on any new regulations about software (for example, IRS could mandate multi-factor auth for all software logins in the future; or new standards for data exchange). Being agile to incorporate such changes ensures longevity.
- **IRS Privacy and Disclosure:** The software must allow the firm to comply with IRS Section 7216 (regulations on use and disclosure of tax return info). If the firm wants to use client data for other services, the software could help generate the consent form for the client to sign. While not a core function, it’s part of compliance environment.

### 16.4 Scalability, Reliability and Availability

- **Scalability:** (Covered in performance) – reiterating that the system can scale up to support growing number of users/clients without major redesign. The cloud infrastructure is designed to add more servers or increase resources transparently. The database can be scaled vertically (bigger instance) and if needed partitioned or sharded for extremely large data loads (likely not needed initially). For on-prem, guide clients to scale hardware if their usage grows.
- **Availability (Uptime):** Target a high uptime especially during critical tax season months. For SaaS, 99.9% uptime goal from January through end of April (meaning minimal downtime, perhaps only brief maintenance windows overnight if absolutely necessary). Off-season, maintenance can be done with slightly more lenience but still aim for >99% year-round.
- **Redundancy:** Deploy redundant components to avoid single points of failure. E.g., use a cluster of application servers behind a load balancer, and a primary-secondary database setup with replication (so if primary DB fails, secondary takes over). Use redundant network, power (if hosting ourselves or rely on cloud provider’s redundancy). This ensures one hardware failure doesn’t take down the service.
- **Backups and Disaster Recovery:** Regular backups (as noted) ensure that even in catastrophic failure, data can be restored. Aim for a Recovery Point Objective (RPO) of at most a few hours (meaning at worst a few hours of data might be lost if a disaster hits between backups). And a Recovery Time Objective (RTO) of a few hours to get the system back up in a DR scenario (like spinning up in a new region if one data center is down).
- **Maintenance Windows:** If maintenance (updates, patches) requires downtime, schedule it during off-peak hours (e.g., 2am Sunday). Communicate to users in advance. Try to use rolling updates to avoid full downtime (for cloud: take one server at a time out, update, then next, so service remains up).
- **Testing Failover:** Periodically test that failover mechanisms work (simulate a server crash to see if secondary takes over).
- **Client-Side Availability:** On-prem deployments rely on the client’s infrastructure. Provide guidelines to them for high availability if they need (like recommending they run the app on a VM cluster or have their own backup strategy). Possibly offer an HA configuration for on-prem (like the app can run on two servers with a shared DB for failover).
- **Capacity Planning:** Monitor usage trends and scale capacity in anticipation of peak (don’t wait until system is at 100% to add resource). Also, after April 15, can scale down cloud resources to save cost (pass savings to pricing or invest in improvements).
- **Service Status and Support:** Provide a status page for the cloud service so users can see if all systems are operational. In case of an outage, post updates there. Have support ready to inform clients and help if their operations are impacted.
- **Cross-Browser and Offline:** Ensure the web app works on all major browsers reliably. If internet is down for a user (cloud scenario), they cannot use until back – as a mitigation, perhaps a limited offline mode could be a future idea (not likely now, but maybe allow working offline and syncing later for on-prem laptop user). At least on-prem gives an offline option inherently (if their network is internal).
- **Longevity:** The software should be maintainable so it remains reliable as codebase grows – meaning keep code modular and clean, so adding new forms or features doesn’t introduce instability. Use automated testing to catch regressions.

### 16.5 Maintainability and Supportability

_(Additional quality considerations)_

- **Maintainable Codebase:** The software should be designed with modular architecture (separate modules for forms, e-file, UI, etc.) so that updates (like adding a new form or fixing a calculation) can be done with minimal impact elsewhere. This reduces bugs and downtime for fixes.
- **Configuration:** Use configuration files or admin UI for things likely to change (tax rates, deadlines). Many of these are data-driven in our design (so updating a tax rate is a data update, not code).
- **Extensibility:** Where possible, design so new features (like a new integration or a new report) can plug in without rewriting core components. For instance, adding a new state form should be as simple as adding its template and rules rather than altering the entire tax logic engine.
- **Documentation:** Provide thorough documentation for users (user guides, context help in the UI) and for administrators (for on-prem install, or for setting up things like the client portal or e-sign). Also internal developer documentation for future maintainers of the software (though that's internal, it ensures future teams can keep it running well).
- **Customer Support Tools:** Build features that help troubleshooting, such as the ability for a support/admin to impersonate a user (with proper logging) to see what they see, or an easy way to extract logs or configuration info from a client’s on-prem system to assist in debugging issues.
- **Issue Tracking and Updates:** Have a mechanism to deploy hotfixes quickly if a critical bug is found (especially in heat of tax season). Possibly an auto-update for minor patches in SaaS (just deploy) and a small patch installer for on-prem that can be applied.
- **Feedback Loop:** Allow users to send feedback or error reports easily (maybe an in-app “Report issue” that attaches context). This helps us catch and fix maintainability issues.
- **Compatibility:** Ensure maintainability by keeping third-party components up to date. Also ensure backward compatibility of data where possible (so an update doesn’t break existing data).
- **Training and Onboarding:** Non-functional but important – support ease of onboarding new users with maybe sample data or templates. If it's easy to learn and use, that speaks to good design (no specific requirement but it's a quality).
- **Environmental Considerations:** Possibly support deployment on various environments without too much tweaking (cloud VM, on-prem Windows or Linux). This flexibility makes maintenance easier because the same code runs everywhere with minor config differences.

In conclusion, the non-functional requirements ensure that the Professional Tax Software not only provides all the needed features but does so with **speed, security, and reliability** expected by professional users. High performance during the crunch time of tax season, rigorous security to protect taxpayer data, strict compliance with all relevant rules, the ability to grow with the user base, and robust operational stability – all these qualities will determine the product’s success and trustworthiness as much as the functional features do.

---

**References:**

- G2 Crowd, _“Best Professional Tax Software”_ – definition of professional tax software and key features.
- IRS Publication 3112 / IRS e-file Provider rules – requirement for software to pass ATS tests.
- Thomson Reuters Tax & Accounting Blog – on digital tax workflow and efficiency gains from e-filing and e-signatures.
- Intuit Accountants (ProConnect) – notes on top 10 factors for tax software, including integration and planning features.
- IRS Publication 1345 – IRS rules for electronic signatures (remote signing with identity verification).
- TaxSlayer Pro Marketing – highlights inclusion of all states, e-filing, bank product integration, etc., as standard in professional suites.
- IRS Safeguards Program – guidance on protecting client data, which informs our security features.

(Note: All citations refer to source content that guided these requirements. In the actual implementation, up-to-date IRS publications and state specifications would be consulted to ensure precise compliance.)
