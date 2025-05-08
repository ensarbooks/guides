# Software Requirements Specification for IncentiveHub Rewards Platform

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) document describes the requirements for **IncentiveHub**, a SaaS-based Rewards and Incentives management platform targeted at product managers and business teams. The purpose of this document is to detail all functional and non-functional requirements for the IncentiveHub platform, including its features, behavior, and constraints. It is intended to serve as a comprehensive guide for stakeholders (product managers, developers, designers, and compliance teams) to understand the system's expected capabilities and design criteria. This SRS will ensure that the final product meets business needs for rewarding customers, employees, and partners through a robust, secure, and user-friendly application.

### 1.2 Scope

The IncentiveHub platform will enable businesses to **digitally source, deliver, and track rewards** (e.g. gift cards, vouchers, tangible gifts) to various recipients such as customers, employees, and partners. It will support a wide range of rewards delivery use cases, including: corporate employee gifting, B2B partner incentives, B2C customer loyalty rewards, and research participation incentives. Key functionalities covered in scope include:

- A **Rewards Catalog** of available digital and physical reward options.
- **Reward distribution** features to send rewards individually or in bulk, with tracking from delivery to redemption.
- **Redemption workflows** for recipients to claim or redeem rewards, and corresponding status tracking.
- **Budget management** tools to define and monitor reward program spending limits.
- **Reporting and analytics** modules to measure reward usage and outcomes.
- **User management and role-based access control (RBAC)** to manage different user roles (e.g., admins, managers, finance) and ensure appropriate access.
- **Audit logging** of key actions for accountability and compliance.
- **Integration capabilities** including public APIs, webhooks, and integration with third-party services (e.g. SSO providers, email/SMS gateways, reward vendors).
- **Compliance and security** features to meet data privacy regulations (GDPR, CCPA) and industry security standards (SOC 2, etc.).
- **UI/UX requirements** for an intuitive web interface and positive user experience, including localization support for multiple languages and regions.

Out of scope for this version are features like internal point-based loyalty currency systems, advanced AI-based reward recommendation engines, or built-in tax reporting for rewards (organizations must handle any tax implications of rewards outside the system). This document focuses on the core requirements to support digital reward delivery and tracking in a multi-tenant SaaS environment.

### 1.3 Product Overview

IncentiveHub is a cloud-based application that provides organizations a centralized platform to manage their rewards and incentives programs. It is primarily intended for **product managers** and other business users who need to incentivize various audiences (employees, partners, customers) without building custom reward solutions from scratch. The platform simplifies the process of procuring rewards (like e-gift cards or vouchers), delivering them to recipients around the world, and tracking engagement (redemptions) — all while managing budgets and ensuring compliance.

IncentiveHub will be offered as a multi-tenant SaaS, meaning multiple business clients (tenants) will use the platform securely in isolation from each other, accessing it via web browsers and integrating via APIs. The product aims to streamline diverse incentive use cases on one platform, increasing efficiency and providing visibility into reward program performance. Key benefits include reducing manual effort in sending rewards, preventing reward fraud or misuse through tracking, and improving recipient satisfaction by offering a variety of reward choices delivered promptly.

### 1.4 Definitions, Acronyms, and Abbreviations

- **SaaS** – Software as a Service. A software distribution model in which a third-party provider hosts applications and makes them available to customers over the Internet.
- **Reward** – A gift or incentive (monetary or non-monetary) given to a recipient (customer, employee, partner, etc.) as part of an incentive program. In this document, rewards typically refer to gift cards, vouchers, promo codes, or physical gifts.
- **Recipient** – The end person who receives a reward (e.g., an employee receiving a gift card, a customer receiving a voucher). Recipients are usually not direct users of the platform but interact via reward redemption links or communications.
- **Catalog** – The collection of reward items available in the platform that users can choose from to send to recipients. This includes digital rewards (e.g., e-gift cards) and tangible items (physical gifts) sourced through integrated providers.
- **Redemption** – The act of a recipient claiming or using a reward (e.g., using a gift card code, claiming a voucher). A reward is considered “redeemed” once the recipient has successfully claimed or used it.
- **Product Manager** – In our context, the primary user persona for this platform: a business user who plans and executes incentive programs (for customers, employees, etc.) to achieve business goals (such as boosting engagement, sales, or survey participation).
- **Administrator (Admin)** – A user role on the platform with elevated permissions, typically responsible for setting up the organization’s account, managing users, configuring integrations, and overseeing all reward programs and budgets.
- **RBAC** – Role-Based Access Control. A method of regulating access to the system’s functions and data based on users’ roles within an organization.
- **GDPR** – General Data Protection Regulation. EU regulation governing data privacy and protection for individuals within the EU. Relevant to how personal data (e.g., recipient information) is handled.
- **CCPA** – California Consumer Privacy Act. A data privacy law in California, USA, similar in intent to GDPR, giving consumers rights over their personal data.
- **SOC 2** – Service Organization Control 2. A compliance standard for service providers, focusing on controls around security, availability, processing integrity, confidentiality, and privacy of customer data.
- **API** – Application Programming Interface. In this context, a set of endpoints exposed by the IncentiveHub platform that allow external systems to interact with it (e.g., to trigger sending a reward programmatically).
- **KPI** – Key Performance Indicator. A metric used to evaluate success; for example, redemption rate of rewards, or total rewards sent in a quarter, could be KPIs for an incentive program.

_(Note: A Glossary in Section 8 provides additional definitions of terms used in this SRS.)_

### 1.5 References

The following references or standards are relevant to the requirements in this document:

- **GDPR (EU Regulation 2016/679)** – Regulation on data protection and privacy in the European Union, which the platform must comply with when handling personal data of EU residents.
- **CCPA (California Consumer Privacy Act of 2018)** – California state law on consumer data privacy, applicable for handling data of California residents.
- **SOC 2 Trust Services Criteria** – Industry standard criteria for managing customer data in the context of security, availability, confidentiality, processing integrity, and privacy. The platform will be developed to meet SOC 2 Type II requirements for security and confidentiality.
- **ISO/IEC 27001** – International standard for information security management. (The platform’s security controls and processes will align with ISO 27001 best practices, though formal certification is a future consideration.)
- **OWASP Top 10** – Open Web Application Security Project Top 10 security risks. The development will consider OWASP Top 10 to ensure mitigation of common web application vulnerabilities (like XSS, SQL injection, etc.).
- **WCAG 2.1 (AA)** – Web Content Accessibility Guidelines version 2.1, level AA. Guidelines for accessible web interface design which will inform UI requirements to support users with disabilities.

### 1.6 Overview of Document

The rest of this SRS document is organized as follows:

- **Section 2 Overall Description:** Provides a high-level overview of the product including its context, user characteristics, assumptions, and dependencies.
- **Section 3 System Features and Functional Requirements:** Detailed description of the platform’s features grouped by functional areas (Catalog Management, Reward Distribution, Tracking, Redemption, Budgeting, User Management, etc.), with specific requirements enumerated for each.
- **Section 4 UI/UX Requirements:** Outlines the user interface and user experience expectations, including key UI features, usability guidelines, and design considerations for the platform.
- **Section 5 Non-Functional Requirements:** Describes requirements related to performance, security, compliance, availability, scalability, maintainability, and other quality attributes the system must fulfill.
- **Section 6 System Architecture Overview:** Presents a conceptual overview of the system’s architecture, including major components, how they interact, and how third-party integrations are incorporated.
- **Section 7 Use Case Scenarios & User Journeys:** Illustrative scenarios and step-by-step user journeys for typical use cases (employee gifting, partner incentives, customer rewards, research incentives), demonstrating how the platform will be used in practice.
- **Section 8 Appendices:** Additional supporting information such as detailed tables for roles and permissions, reward type examples, and a glossary of terms. (Any detailed data or lists that support the requirements are included here for reference.)

Each requirement in this document is uniquely identified and described. Functional requirements are generally labeled “FR” (for example, FR-1, FR-2) and non-functional requirements as “NFR” where needed, though for readability they may be presented in bullet or tabular form rather than a single exhaustive list. This document is intended to be updated as the project evolves, with version control to track changes in requirements.

## 2. Overall Description

### 2.1 Product Perspective

IncentiveHub is a **new, standalone SaaS application** developed to streamline rewards and incentives management. It is not a component of an existing product but will integrate with various external systems (e.g., email/SMS services, SSO identity providers, and reward suppliers) as needed. The platform adopts a **multi-tier architecture** and a **multi-tenant model**, meaning a single instance of the application serves multiple client organizations, with data partitioning to ensure each organization’s data is isolated and secure.

From a **product perspective**, IncentiveHub acts as a central hub that connects those who **issue rewards** (the business users/administrators) with those who **receive rewards** (employees, customers, partners), along with the vendors who **fulfill rewards** (gift card providers, etc.). It sits between the business and the reward fulfillment channels:

- Upstream, it interfaces with **business systems and users** (e.g., a product manager using a web UI or an external application calling the API to trigger a reward).
- Internally, it manages business logic like selecting rewards from the catalog, logging transactions, enforcing budgets, etc.
- Downstream, it connects to **delivery mechanisms** (such as email or other messaging services to send reward links/codes) and to **reward providers** (e.g., third-party gift card services or vendors that supply the actual reward items).

The platform’s design will be modular, consisting of components for catalog management, reward processing, user management, etc. It will leverage cloud infrastructure for scalability and reliability. Figure 6.1 in the System Architecture section provides a high-level visual overview of how these components interact within the environment.

### 2.2 Product Functions

At a high level, the key functions of the IncentiveHub platform include:

- **Reward Catalog Management:** Provide a comprehensive catalog of reward options (e.g., gift cards to various retailers, prepaid vouchers, merchandise) which users can browse and choose from. This includes maintaining item details (description, value, category, availability region, etc.) and updating availability or adding new reward types as needed.

- **Reward Issuance (Delivery & Distribution):** Enable users to send rewards to recipients easily. This covers single reward sending (ad hoc rewards) and bulk distribution (mass incentives), scheduling deliveries, personalizing messages, and choosing delivery methods (email, SMS, etc.). The system handles interacting with external providers to actually fulfill the reward (e.g., calling an API to generate a gift card code) and deliver it to the recipient.

- **Reward Tracking & Lifecycle Management:** Track each reward from the moment it’s initiated to the point it’s redeemed (or expires). The system logs statuses like sent, delivered, opened, redeemed, or failed. Users can monitor reward delivery in real-time, see which rewards are unclaimed, send reminders, or cancel/reissue rewards if needed.

- **Reward Redemption Support:** Provide a smooth experience for recipients to redeem their rewards. This includes hosted redemption pages or links where recipients can view their reward (e.g., reveal a gift card code or enter shipping information for a physical gift), choose from multiple reward options if offered, and confirmation of redemption. The system ensures that each reward can only be redeemed once and handles any errors (e.g., an expired link or an already-used code) gracefully.

- **Budget Management:** Allow organizations to allocate and manage budgets for their rewards programs. Users (especially finance or admins) can set spending limits (overall or for specific campaigns/teams), track the amount spent vs. remaining budget, enforce limits (prevent or require approval for actions exceeding budget), and adjust budgets as needed. The platform may support multiple budget categories or periods (e.g., quarterly budgets, campaign-specific budgets).

- **User Management and RBAC:** Provide administrative functions to manage user accounts within each organization using the platform. This includes creating users, defining roles/permissions (e.g., admin, program manager, viewer), and controlling access to features and data based on role. For example, one user may have rights to send rewards and manage campaigns, while another can only view reports. Additionally, the system will integrate with single sign-on solutions to streamline authentication where needed.

- **Audit Logging:** Record a detailed audit trail of important actions in the system for security and compliance. This includes logging user activities such as login attempts, reward distributions, changes to budgets, modifications of user roles, and configuration changes. Audit logs are accessible to authorized users (e.g., admins) to review who did what and when, supporting accountability and external compliance audits (like SOC 2).

- **Reporting and Analytics:** Offer reporting tools and dashboards for users to analyze the performance of their reward and incentive programs. Key metrics include number of rewards sent, redemption rates, total spend, budget utilization, and program ROI indicators. Users should be able to generate summary reports (with charts) and detailed logs (with data export) to evaluate effectiveness and present results to stakeholders.

- **APIs and Integrations:** Provide external interfaces to integrate the IncentiveHub platform with other systems. This includes a robust RESTful API for triggering rewards and retrieving status programmatically (useful for integration into customer applications or workflows), as well as webhooks or callbacks to notify external systems of events (like a reward redeemed). Integration capabilities also cover connecting with third-party services such as email/SMS gateways (for delivery), SSO identity providers (for user login), HR or CRM systems (for importing recipients), and reward vendors (for sourcing the rewards).

- **Compliance and Security Features:** Ensure the platform operates within required legal and security frameworks. This includes protecting personal data (encryption, access control), obtaining necessary consents or providing opt-outs for communications if needed, allowing data deletion or export per GDPR/CCPA rights, and maintaining high security standards (secure coding, penetration testing, etc.). Role-based access and audit logs (as mentioned) contribute to this, as do features like configurable data retention policies.

- **Localization and Multi-Currency Support:** Support multiple languages and regional settings in the UI and in reward offerings. For example, a user should be able to view the interface in English, Spanish, French, etc., and send rewards that are appropriate for the recipient’s country (both in terms of language of the message and type of reward/currency). Date/time formats, currency conversion for budgets, and other localization aspects will be handled to make the platform usable globally.

These functions will work together to provide a seamless end-to-end solution for incentive management. In practice, a product manager could log into IncentiveHub, create a campaign (with a defined budget), select a set of rewards from the catalog, send those rewards to a list of recipient emails (either manually or via an integration trigger), and then use the platform to monitor who redeemed their rewards and how much budget remains, all within one system.

### 2.3 User Classes and Characteristics

The platform will be used by several distinct user classes, each with different needs and permissions. Below are the primary user roles (within a client organization) and their characteristics:

- **Organization Administrator (Org Admin):** This user class represents the primary administrator(s) of the platform for a given client organization. Typically an IT lead or a program owner, the Org Admin has the highest level of permissions within their organization’s tenant. They can manage all aspects of the account: user accounts and roles, global settings, budgets, integrations, and have full visibility into all reward campaigns and data. They ensure the platform is configured properly (e.g., SSO integration, adding company branding elements, setting default settings). They are also responsible for creating other user accounts (managers, viewers, etc.) and assigning appropriate roles. Characteristics: tech-savvy, security-conscious, needs full control; likely relatively few people (one or two per organization).

- **Program/Rewards Manager:** This is the primary user type for which the platform is targeted (often the _product manager_, marketing manager, HR manager, or whoever runs the incentive programs). Rewards Managers are the users who create and manage reward campaigns. They select rewards from the catalog, define recipient lists or criteria, send out rewards, and monitor their campaigns’ progress. They have access to create and edit campaigns, view results for their campaigns, and generally manage day-to-day operations of reward distribution. Depending on organizational setup, a Rewards Manager might only see campaigns they created or those for their department, or they might have access to all campaigns (if not limited by role scope). Characteristics: business-oriented, goal-focused (wants to increase engagement, etc.), expects an easy-to-use UI to quickly send rewards and check status; not necessarily deeply technical.

- **Finance/Budget Manager:** In some organizations, financial controllers or budget owners may use the platform to oversee spending. This user class focuses on the **budget management** and **reporting** aspects. They set up budgets or cost centers for reward programs, approve or monitor expenditures, and run spend reports. They might not initiate reward sends themselves but need visibility into how funds are used. They typically have permissions to adjust budgets, view all transactions, but perhaps not to create campaigns (depending on internal policy). Characteristics: detail-oriented, concerned with cost control and ROI, may use export reports for accounting reconciliation.

- **Viewer/Read-Only User:** This class includes any stakeholders who need to see information on the platform but not make changes. For instance, an executive or a client of the business might be given read-only access to dashboards to observe program performance. Or a compliance officer might be given access to audit logs. These users can log in and navigate through reports, campaign statuses, etc., but cannot trigger any actions (no sending rewards, no editing). Characteristics: could be high-level (needs summary information) or support role (needs to verify data), will use primarily the reporting UI or read-only views.

- **Recipient (External User):** Technically not a user of the platform in the sense of logging into the main application, but they are a crucial actor. Recipients are employees, customers, partners, or research participants who receive the rewards. Their interaction is via the **redemption process** – for example, clicking an email link to claim a gift card. They expect a simple, quick way to get their reward without needing an account or complicated steps. The platform must cater to recipients by providing a user-friendly redemption page (web interface, likely mobile-friendly) and possibly choices of reward. We consider their needs in the design of the redemption workflow (clear instructions, support if issues, etc.). Recipients vary widely in background (could be tech-savvy or not, internal or external to the company), so that part of the system must be extremely simple and reliable.

- **System Administrator (Platform Operator):** (This is an internal role, not within a client organization, but worth mentioning for context.) The team running the IncentiveHub service (the vendor or IT ops) will have superuser access to manage the overall system, configure the reward catalog, and oversee multi-tenant operations. They are responsible for uploading new rewards to the global catalog, maintaining integrations with suppliers, and handling any global configuration (like turning features on/off, doing system maintenance). This SRS primarily addresses requirements for client-facing functionality, so this role’s needs (like internal admin tools to manage the catalog) are mentioned where relevant but not a focus of this document’s scope.

**Roles and Permissions:** The platform will implement role-based access control to manage what each user class can do. A summary of roles and their permissions is illustrated in **Table 3.6.1** in section 3.6. In general, Org Admins have all permissions within their org; Program Managers have permissions to manage rewards/campaigns and view related data; Finance Managers have permissions around budgets and financial data; Viewers have view-only access to designated sections. These roles might be configurable per organization (for example, an organization might decide to merge program and finance roles for a single user, or require dual approval for some actions – such specifics can be configured on top of the base roles).

### 2.4 Operating Environment

The IncentiveHub application will operate in a **cloud-based environment** accessible primarily via web browsers. Key aspects of the operating environment include:

- **Client Side:** Users will access the platform through a secure web application. The web app will be compatible with modern web browsers (at minimum, the latest versions of Google Chrome, Mozilla Firefox, Microsoft Edge, and Safari) on desktop operating systems (Windows, macOS, Linux). The UI will be responsive to support use on various screen sizes, including tablets and smartphones, although primary usage is expected on desktop for administrative tasks. No software installation is required on client machines; only an up-to-date browser and internet connection. The interface will use standard web technologies (HTML5, CSS3, JavaScript). For mobile recipients (e.g., an employee opening a reward link on their phone), the redemption pages will be mobile-friendly via the responsive design, but there will not be a separate native mobile app in the initial scope.

- **Server Side:** The platform’s server-side components will be hosted on a cloud platform (e.g., AWS or Azure). It will likely consist of application servers (running the web backend and APIs), database servers for persistent storage, and ancillary services (for caching, message queuing, etc.). The environment will have separate instances for development, testing, staging, and production to allow safe development and deployment practices. Production environment will be scalable across multiple servers/instances to handle load and provide redundancy. Operating systems used on servers will be appropriate for the chosen tech stack (likely Linux-based for web servers). The database is expected to be a relational DBMS (such as PostgreSQL or MySQL) for core data, with potential use of NoSQL or in-memory stores for specific needs (like caching catalog data or storing session info).

- **Network and Security:** The application will be accessed via HTTPS over the public internet. It will enforce TLS 1.2+ for all communications to ensure data in transit is encrypted. The service endpoints (web and API) will sit behind a load balancer and possibly a web application firewall (WAF) for security. Integration points to external services (like reward providers or email gateways) will also be over secure APIs. The environment will include monitoring and logging infrastructure to track performance, errors, and security events. The system will be deployed across multiple availability zones or data centers to ensure high availability (detailed in Section 5.4).

- **Constraints from Operating Environment:** Since it’s SaaS, the system must be multi-tenant, meaning careful separation of data by tenant in the database and proper authentication to ensure users only access their organization’s data. The environment will likely use containerization or virtualization for deployment, which implies that the software should be stateless where possible (session state stored in a shared store or sent to client) to allow horizontal scaling. The cloud environment also provides the ability to auto-scale resources based on usage patterns, which the application should be designed to leverage (for example, background processing workers scaling up if many reward emails need sending). All these factors impose design constraints (like using stateless services, externalizing configuration, etc.) which are considered in architecture, but from a requirements perspective, it means the system must **behave correctly in a distributed, dynamic cloud environment** and maintain consistency and performance as it scales.

### 2.5 Design and Implementation Constraints

The development of IncentiveHub must consider several constraints:

- **Regulatory Compliance:** As a major constraint, the system design must ensure compliance with GDPR, CCPA, and other privacy/security laws. This affects how data is stored (e.g., using encryption for personal data), data residency if required (e.g., EU user data may need to reside in EU data center if clients demand), and features like data deletion or anonymization. It also influences UI (e.g., showing privacy notices or obtaining consent for tracking if needed).

- **Security Standards:** To achieve SOC 2 compliance and overall robust security, certain design constraints are imposed. For example, all user authentication must be designed to allow integration with SSO (SAML/OAuth2) and enforce strong password policies for non-SSO logins; all actions need to be permission-checked (RBAC) which influences how the application logic is structured; audit logging must be built into the system from the start since retrofitting it is hard. The system must also avoid storing sensitive data unnecessarily (for instance, do not store plaintext reward codes if not needed, do not store credit card information at all by using external payment processors).

- **Technology Stack Decisions:** The choice of tech stack might impose constraints. For instance, if the team chooses a certain web framework or database, there might be limitations on maximum data throughput or specific libraries available for features like PDF generation of reports, etc. While this SRS does not dictate implementation tech, it assumes the solution will use proven enterprise technologies that support required features (e.g., a robust scheduling library to schedule future sends, or a reliable job queue for handling bulk email sends). If any third-party components are to be used (like a particular gift card provider’s SDK), compatibility and licensing could be constraints.

- **Multi-tenancy and Scalability:** The system must be designed as multi-tenant from the ground up. This is a constraint meaning every database query or data model must include tenant isolation (like an Org ID). Also, heavy operations (like sending thousands of emails) must be handled asynchronously to not block UI, implying the need for a message queue or background worker system – this is an architectural constraint that influences design (we cannot do everything in a single request/response thread). The constraint ensures that one tenant’s heavy usage doesn’t starve others (so proper resource management, maybe per-tenant rate limiting might be needed at some level).

- **Integration Constraints:** The platform will integrate with external services (SSO, email, reward providers). We are constrained by those services’ availability and API limits. For example, a gift card provider might have a rate limit on API calls or a certain format for requests/responses we must adhere to. The design must accommodate retries and fallbacks if an external service is down. Also, the system should be flexible to swap out providers – e.g., if we initially integrate Provider A for gift cards but later need Provider B, the integration layer should be abstracted (likely a constraint to use a plugin/adapter pattern for reward providers).

- **UI/UX Constraints:** The UI should follow the company’s design language and be consistent. If there are existing style guides or branding requirements for the platform, they must be followed. Also, accessibility standards (WCAG) impose constraints like color contrast and keyboard navigation requirements. Additionally, since product managers are busy individuals, the UI should be optimized for efficiency – a constraint might be “no process for sending a reward should take more than N clicks” or “the system should respond to any user action within 2 seconds to maintain responsiveness,” which influences design and performance considerations.

- **Time and Release Constraints:** (Project management constraint) If this SRS corresponds to an initial version release, some features might be prioritized or deferred. For example, perhaps full localization might be planned but only English is delivered in version 1, with the framework in place for others. These kinds of constraints (phased implementation) are typically documented to manage stakeholder expectations, but for this SRS we assume the end vision of the product. If needed, it can be noted that certain features are “Phase 2” or optional.

In summary, the constraints highlight that the platform must be built with security, compliance, and scalability in mind from day one, using an architecture conducive to multi-tenant cloud deployment, and a UX that meets enterprise usability standards. All of these constraints have influenced the requirements detailed in Section 3 onward.

### 2.6 Assumptions and Dependencies

To clarify the requirements, the following assumptions and external dependencies are noted:

- **User Base Assumptions:** It is assumed that users of the platform (Admins, Managers, etc.) will have basic internet and web application proficiency. No advanced technical knowledge (like programming) is required for normal operation. For recipients, we assume they have access to email (or other communication used to send the reward) and internet access to redeem their reward. We also assume recipients trust the sender enough to click the reward link (hence the importance of allowing companies to customize branding on communications to reassure recipients).

- **Reward Fulfillment Partners:** The platform depends on third-party **reward providers** (e.g., gift card aggregators, retailers, or fulfillment companies) to actually fulfill the rewards. We assume that these providers offer reliable APIs or services to procure digital codes or trigger physical shipments, and that they will provide inventory of rewards (e.g., a selection of gift card brands) as agreed. The list of available rewards in the catalog is therefore dependent on partnerships or integrations with these external systems. If a provider changes their API or a certain reward becomes unavailable, timely updates on our side will be needed (this is a dependency risk). We plan to integrate with well-established providers that offer a wide catalog (for example, a gift card API that provides hundreds of brand options globally).

- **Email/SMS Delivery:** We assume the availability of robust email and SMS gateway services for delivering reward notifications. The platform will integrate with an email service (like SendGrid, SES, etc.) and possibly an SMS service for text message delivery. It is assumed that recipients’ email addresses and phone numbers are valid and that emails/texts will successfully reach them. However, as bounce-backs can happen, the system will handle undeliverable messages (the dependency is that we receive bounce notifications or can query status from the email service).

- **Integration with Client Systems:** We assume that for features like Single Sign-On, the client organization will provide necessary information (e.g., their SAML identity provider details) and that their environment supports standard protocols. Similarly, if the platform is to import data from an HR or CRM system, it’s assumed those systems have an export or API capability that can be used (or at least the client can provide CSV files in a consistent format). While the platform will provide APIs and import tools, the usefulness is dependent on the client’s ability to use them or their IT support to integrate.

- **Budget and Finance:** We assume that companies using the platform will handle funding of rewards externally (e.g., via prepaid deposits or being billed). The platform will track spending against budgets but likely will not handle actual payment processing for each reward in the initial phase. Instead, we assume either a pre-funded model (the company prepays an account from which rewards draw down) or a post-pay model (the company is invoiced for rewards sent). In either case, our system might integrate with a payment gateway or have an internal billing subsystem (especially if prepay with credit card). It’s assumed the volume of transactions and payment amounts will be within normal business ranges and not trigger unusual financial compliance issues (like anti-money-laundering checks, since these are gifts, not direct monetary transactions between private parties, and values are typically modest).

- **Legal/Compliance Use by Clients:** We assume that clients will use the platform for legitimate purposes of rewarding and have obtained any necessary consent from recipients to contact them. For instance, if a business is sending a reward to a customer, we assume that the customer has agreed to receive communications (or at least that sending a one-time reward email is within permissible communication under that business relationship). The platform will provide tools to comply (like opt-out management or including an explanation in the email of why the person is receiving a reward), but it assumes the client bears responsibility for the legality of whom they choose to send rewards to.

- **Dependency on Time and Regional Settings:** We assume that the system clock and time zone settings in the environment are properly configured (likely using UTC internally and converting to local time zones in UI) so that scheduling and time-stamping functions work correctly. Also, currency exchange rates (if needed for currency conversion in multi-currency budgets or showing equivalent values) will be fetched from a reliable source – this is a dependency on an external forex rate API if that feature is implemented.

- **Hardware and Scaling:** We assume that the cloud infrastructure can scale to meet our needs, given proper configuration. The system is expected to handle potentially tens of thousands of rewards being processed (sent or redeemed) per day across all tenants, but should usage exceed expectations, we assume the infrastructure (with possible vertical or horizontal scaling) can be upgraded without requiring fundamental software changes. This is tied to using scalable services (like managed databases that can be upgraded, or auto-scaling groups for application servers).

In summary, the success of the platform is dependent on cooperation between it and external services (for identity, communication, and reward fulfillment) and on clients using it as intended within legal bounds. These assumptions and dependencies will be revisited periodically; if any assumption proves false, requirements might need adjustment (for example, if clients demand integrated payment handling, that would become an additional requirement in a future phase).

## 3. System Features and Functional Requirements

This section details the functional requirements of the IncentiveHub platform, grouped by major feature areas. Each subsection describes a feature or module of the system, followed by specific requirements. The requirements are written in a descriptive manner; key requirements are highlighted with “**The system shall…**” or **FR-x** for clarity. Tables and lists are used to summarize certain sets of requirements (e.g., user roles, reward types) where appropriate.

### 3.1 Reward Catalog Management

**Description:** The Reward Catalog is a core component providing an organized list of all reward options that can be delivered through the platform. It includes digital rewards (like e-gift cards, e-vouchers, coupon codes) and physical rewards (like merchandise or gift items) that can be sourced and fulfilled. Product managers (and other users) will browse this catalog when choosing rewards to send. The catalog may be global (managed by the platform provider) but should be filterable and configurable per client (e.g., an organization might disable certain reward types or add custom rewards of their own). This section describes how the catalog is managed and presented.

Key capabilities include viewing reward details, searching and filtering the catalog, selecting rewards (for sending or to include in a campaign), and possibly customizing certain reward entries (like adding a custom description or company-specific items). The catalog data will be populated via integration with external suppliers or manual input by a system admin. For digital rewards, inventory is typically not limited (codes are generated on demand via provider), but for physical items or limited stock items, availability needs to be indicated. Pricing information (cost to the company for each reward) also needs to be shown for budgeting purposes.

**Functional Requirements:**

- **FR 3.1.1 Catalog Listing:** The system shall provide a user-friendly **Catalog page** where users can browse all available rewards. Each catalog item shall display key information such as reward name, category (e.g., “Electronics Gift Card” or “Travel Voucher” or “Merchandise”), value or denomination (e.g., $50, or specific item description), and type (digital vs physical). If relevant, a thumbnail image or logo for the reward (e.g., the retailer’s logo for a gift card) shall be shown to help users quickly recognize the brand or item.

- **FR 3.1.2 Reward Details:** The system shall allow users to click on or select a reward item to view its **detailed information**. This includes a description of the reward, terms and conditions (if any, e.g., “card expires in 1 year” or “valid only in US stores”), available denominations (for gift cards, if multiple values are available), delivery format (e.g., “Code delivered via email” or “Physical shipment”), and **cost information**. The cost information should clarify what sending this reward will deduct from the budget. For example, if a $50 gift card has no additional fees, the cost is $50; if a physical item has shipping or fulfillment fee, it should indicate the total cost. If the platform charges a service fee, that might be factored in (though in many cases, cost = face value for simplicity).

- **FR 3.1.3 Search and Filter:** The system shall provide **search and filtering** functionality on the catalog. Users shall be able to search by reward name or keyword (e.g., “Amazon” to find Amazon gift cards) and filter by categories such as:

  - Reward Type: Digital vs Physical.
  - Category/Industry: e.g., Retail, Food, Travel, Experience, Charity (donation vouchers), etc.
  - Value Range: filter rewards by their monetary value or cost (e.g., show only rewards worth $100 or less).
  - Region/Currency: filter to show rewards available in certain regions or currencies (e.g., show only rewards that can be redeemed in Europe, or only rewards in USD).
  - Vendor/Brand: if relevant, a filter by vendor (all rewards from a specific provider).

  These filters help narrow down choices, especially as the catalog could contain hundreds of items.

- **FR 3.1.4 Availability by Region:** The system shall handle region-specific availability for rewards. Each reward item in the catalog shall have metadata indicating in which countries or regions it can be delivered or redeemed. For example, a “$50 Amazon.com Gift Card” might be tagged as only redeemable in the US, whereas an “Amazon.de Gift Card” is for Germany. When a user is planning to send a reward to recipients in a certain country (which the user might indicate by choosing locale or the recipients’ info might have country), the system should help by filtering or warning if a selected reward is not suitable for the recipient’s region. _(If the platform doesn’t know recipient region at selection time, at least a note in the reward detail should say “Valid in US only”.)_

- **FR 3.1.5 Custom/Client-Provided Rewards:** The system shall allow for **custom rewards** to be added by an organization (if they have something unique to offer). Examples: a company might want to offer “Company Branded Swag Box” that they will fulfill internally, or “Extra Day Off Certificate” as a reward for employees. These are not sourced from the global catalog providers. For such cases, an Org Admin should be able to create a new reward entry visible only to their organization’s users. The entry would have a name, description, perhaps an upload of an image, and a way to mark how it’s fulfilled (could be “manual fulfillment” which just records that someone chose it and then the company takes action offline). This is an advanced feature and may be optional; if implemented, the system will clearly mark custom rewards vs standard ones. Custom rewards still need to be tracked (e.g., if someone selects it, mark it as redeemed or fulfilled manually by admin later). This requirement ensures flexibility for unique incentive ideas beyond the standard catalog.

- **FR 3.1.6 Catalog Update and Synchronization:** The system shall regularly **update the catalog** entries via its integration with external providers. If a provider adds new gift card brands or if an item becomes unavailable, the changes should reflect in the catalog. This might happen via automated sync (e.g., a daily job to fetch current catalog from provider API) or via manual input by a system administrator. From the user perspective, the catalog is always up-to-date. If a user tries to select a reward that just went out-of-stock or is discontinued, the system shall either hide it or inform the user upon selection attempt and prevent sending it. (This is closely tied to error handling in the sending process, but it starts with having current catalog data.)

- **FR 3.1.7 Pricing and Currency Handling:** The catalog should display reward values in a way that’s clear to the user. For monetary rewards (like gift cards), the “value” is typically the same as cost (e.g., a $50 gift card costs $50). For foreign currency gift cards, the system might list them as “£50 British Airways Voucher” and if the user’s budget base currency is different, it may also show an approximate conversion (optional). **The system shall support multi-currency display**: if a user’s organization base currency is USD but they are viewing a reward in EUR, the system could show “€50 (approximately $55)” based on latest exchange rates for informational purposes. (Actual billing may happen in base currency – more in Budget section.) This helps product managers understand cost implications. If real-time conversion is complex, at minimum the system shows the value in the reward’s native currency and a note that currency conversion may apply.

- **FR 3.1.8 Permissions for Catalog Viewing:** Generally, all logged-in users in an org (except perhaps some restricted viewer roles) should be able to view the catalog. The system shall allow configuration such that some roles (like a Viewer) might not need to see all details. But likely, catalog is accessible to Program Managers and Admins who actually send rewards. If needed, an admin could restrict certain categories for their organization. For instance, an admin might toggle off “Alcohol” category gift cards if that doesn’t align with company policy. **The system shall provide Org Admins the ability to configure catalog visibility** by category or item (basically hiding certain reward types from their organization’s view), to enforce their internal policies. This is an optional but useful control.

- **FR 3.1.9 Catalog Performance:** The system shall be optimized so that browsing the catalog is fast and responsive. Even if there are hundreds of items, users should be able to find items quickly (through search/filter as above). This is more of a performance consideration, but from a functional perspective, the catalog queries should be efficient. If needed, paging or infinite scroll can be used to not overload the page. This requirement ensures a smooth browsing experience.

- **FR 3.1.10 Content Management for Catalog:** The text and images in the catalog may need to be updated (e.g., a description change or uploading a new image for an item). This will be done by the platform’s internal team or via the integration. The system shall allow updates to catalog content without requiring a full software release (for instance, through an admin interface or by re-sync from provider data). If a reward is temporarily unavailable, the system should mark it as such (e.g., “Out of stock” label) or hide it. Users attempting to select it should be prevented. This ties into reliability of the catalog data.

**Table 3.1 - Examples of Reward Types in Catalog:**  
To illustrate the diversity of the catalog, below is a table of example reward types that IncentiveHub might offer and their characteristics:

| **Reward Type**             | **Description**                                                                                                                          | **Delivery Method**                                         | **Example Items**                                                               |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Digital Gift Card**       | Prepaid cards for retailers or services, delivered as codes or electronic vouchers.                                                      | Code via Email/SMS (digital)                                | Amazon gift card, Starbucks e-card, Uber voucher                                |
| **Physical Gift**           | Tangible items or merchandise sent to recipient’s address. Often fulfilled via a partner or e-commerce integration.                      | Shipped to Address (physical)                               | Company swag box, Books, Electronics gadget (e.g., headphones)                  |
| **Prepaid Visa/Mastercard** | A general-purpose prepaid debit card, loadable with a specified amount, often branded.                                                   | Physical card mailed, or digital code (digital or physical) | $100 Prepaid Visa Card (digital claim or mailed plastic card)                   |
| **Experience Voucher**      | Tickets or vouchers for experiences (travel, events, etc.)                                                                               | Email with booking code or instructions                     | Airline ticket voucher, Hotel gift certificate, Concert tickets code            |
| **Donation/Charity Gift**   | A charitable donation made on behalf of the recipient to a chosen charity. Often offered as an option to donate equivalent reward value. | Email confirmation (digital)                                | $50 Donation to Red Cross (recipient typically gets a note of thanks)           |
| **Coupon/Promo Code**       | A code granting discount or free service in a product (could be the company’s own product). Used as B2C incentives.                      | Code via Email (digital)                                    | 20% off next purchase code, Free month subscription code                        |
| **Custom Reward**           | Company-specific incentive defined by the user organization. Fulfillment might be manual or outside platform.                            | Varies (could be email certificate)                         | “Lunch with CEO” coupon, “Extra Vacation Day” certificate, “Custom Gift Basket” |

_Table 3.1_ – The platform’s catalog can include a wide range of reward types. Each type has different fulfillment methods and use cases. The system architecture (especially integration) must handle each appropriately (e.g., interfacing with gift card API for digital cards, or prompting for address for physical gifts). The catalog will categorize these so users can easily choose suitable rewards for their audience.

### 3.2 Reward Delivery and Distribution

**Description:** This feature covers the process of sending rewards to recipients. Product managers or other authorized users will initiate reward delivery through the platform. This can happen in various ways: individually sending a reward to a single recipient (ad hoc gifting), sending in bulk to a list of recipients (mass distribution for a campaign), or automatically via triggers through the API (for example, a customer completes a milestone and the system sends a reward without manual intervention). The platform must handle all these cases in a user-friendly and reliable manner.

When sending a reward, the user typically will: choose the reward from the catalog, specify details (such as value if applicable, quantity if multiple recipients, and any message), specify the recipient(s) (enter emails or select a pre-uploaded list), and then confirm sending. The system then orchestrates the fulfillment: contacting the reward provider to generate the gift (if needed) and delivering the notification (usually via email) to the recipient with instructions or a link to redeem. This sub-system also deals with scheduling (send now or at a future date), personalization of messages, and ensuring that the sending action is logged and reflected in budgets.

**Functional Requirements:**

- **FR 3.2.1 Single Reward Sending:** The system shall allow a user to send a reward to a single recipient in a straightforward workflow. For example, a Product Manager can choose “Send Reward” from the dashboard, then: select a reward from the catalog (e.g., $50 Gift Card), enter the recipient’s details (at minimum, an email address; possibly name and a personal note), and confirm. The system shall then process this request by reserving or generating the reward (through the provider API) and sending an email to the recipient with the reward details or a link to redeem (depending on how the specific reward type is delivered). This process should ideally be done in a few simple steps (usability focus). After sending, the user should see a confirmation that the reward was sent successfully (or an error message if something went wrong).

- **FR 3.2.2 Bulk Rewards Sending (Batch Distribution):** The system shall support sending a reward (or set of rewards) to multiple recipients in one operation. Users (with permission) can initiate a **bulk send** by either selecting multiple recipients or uploading a list. Requirements for bulk:

  - The user can specify a list of recipients. This can be done by uploading a CSV file containing recipient identifiers (e.g., email, name, maybe other fields like employee ID), or by selecting a pre-defined group (if the system has groups of recipients stored), or manually entering multiple emails in a form field separated by commas.
  - The user selects the reward (or possibly multiple different rewards if each recipient gets something different? Usually, bulk send is same reward to many people. If per individual customization is needed, separate sends or an upload that contains which reward each gets might be supported).
  - The user can compose a single message template that will be sent to all (with placeholders for personalization like recipient name, if provided). **The system shall support message templates** with basic placeholders like {{FirstName}} for personalization in bulk sends.
  - The system shall validate the list before sending: e.g., check that email addresses are in proper format, remove duplicates, and perhaps cross-check against a do-not-send list (if someone opted out, see compliance).
  - Upon confirmation, the system will iterate and send each reward. Since this could be hundreds or thousands, it should be handled asynchronously (e.g., put into a job queue). The user should be informed that the send is in progress and possibly given a way to monitor it (like “500 of 1000 emails sent” progress, or at least an email/notification when done). Alternatively, for moderate sizes, it might process quickly enough to just confirm success with a summary.
  - **FR 3.2.2a**: The system shall set an appropriate status for each reward sent in bulk and allow the user to download a report or view a list of recipients and status after the bulk operation, so they know if any failed.

- **FR 3.2.3 Scheduling Rewards:** The system shall offer an option to **schedule a reward send for a future date/time**. For example, an HR manager may schedule birthday e-cards ahead of time or a product manager might schedule sending all rewards on a specific holiday or campaign launch day. When scheduling, the user will pick the date and time for the send. The system must store this and ensure the rewards are sent at approximately that time. (Given that at send time, it will need to fetch codes or such, it should do so at the scheduled time, not upfront, to ensure validity and minimize early cost if applicable.) The system should show scheduled outgoing rewards in a list (so user can confirm or cancel them before they go out). **The system shall ensure that scheduled rewards do not exceed budget at time of sending** – which means, if a reward is scheduled but later budget changes, we need logic: either reserve budget when scheduling or re-check at send time. Perhaps simplest is to deduct budget when scheduled (so it’s accounted for), but then if cancelled before actual send, budget should be released. This is a detail to manage.

- **FR 3.2.4 Personalized Messaging:** For each reward sent (single or bulk), the system shall allow the sender to include a **personalized message** to the recipient. This could be a custom note like “Thank you for your great work on Project X!” or “Happy Holidays, enjoy this token of appreciation.” In bulk sends, if a personalization field is provided per recipient (like their achievement or reason for reward), perhaps template could include that, but that might be too granular. Realistically, in bulk, the message is generic or only name-personalized. For individual sends, fully custom message each time. The system should include this message in the reward notification (email or other channel). The message should support simple text, possibly limited formatting (like bold, italics, or adding an image/logo which might be automatically included as part of email template rather than per message content). This requirement ensures that communications feel personal and aligned with the sender’s tone.

- **FR 3.2.5 Delivery via Multiple Channels:** The primary channel is Email, but the system shall also support alternative delivery channels where applicable:

  - **Email:** Default method – the system sends an email to the recipient’s email address, containing either the reward details (like an e-gift card code embedded) or a button/link to a redemption page.
  - **SMS:** If a mobile number is provided and the reward type is conducive to SMS (like a short code or a link), the system should allow sending a text message with the reward link/code. (E.g., for on-the-spot incentives where phone is used, or for populations who respond better to SMS).
  - **In-App/Link Delivery:** For cases where the platform’s API is used, a product’s own application might deliver the reward info in-app. In such scenarios, the system might not send an email itself but instead provide the code or redemption link via API response, which the client app then displays to the user. So effectively, the channel is the client’s application. This is covered in API section but noted here as a method.
  - **Printed/Other:** Unlikely, but just in case: maybe allow exporting an award certificate PDF which can be printed and handed (like for employee awards ceremonies). Could consider an option to generate a PDF certificate for a reward (nice to have).

  The requirement is that the system design should not hard-code only email; it should be extensible to at least SMS and possibly push notification (if a mobile app integration exists later). At launch, Email will be primary with SMS as an optional add-on.

- **FR 3.2.6 Confirmation and Notifications:** When a user (sender) triggers reward delivery, the system shall provide appropriate confirmations:

  - After a single send, show a success message like “Your reward has been sent to [recipient email]” or if scheduled, “Your reward is scheduled to be sent on [date]”.
  - For bulk sends, possibly show “Your rewards are being sent to X recipients. We will notify you when sending is complete.” and perhaps an email or notification in the app once done.
  - If any sends fail (like an invalid email address format in bulk), the system shall notify the user which ones failed and why (and possibly allow a retry after correction).
  - The system should also log this action (for audit and for later viewing in tracking).
  - Optionally, a user might opt to get an email summary of their bulk send results or upcoming scheduled sends as reminders.

- **FR 3.2.7 Prevention of Duplicate Sends:** The system shall help avoid accidental duplicate sending of the same reward. For instance, if a user clicks send twice accidentally, there should be a safeguard (like disabling the send button after first click, which is a UI consideration, and on backend maybe check duplicate request). If a user tries to send the exact same reward to the same recipient twice in a short period, perhaps warn “You have already sent a $50 gift card to this email today. Are you sure you want to send another?” (This might be a safety feature to prevent mistakes but should be overrideable because sometimes you do want to send multiples.)

  - Additionally, in bulk, if the list has duplicate emails, either automatically de-duplicate or alert user and ask if they meant to send multiple to one person.

- **FR 3.2.8 Throttling and Batch Processing:** For large bulk sends (e.g., thousands of recipients), the system shall send messages in batches to avoid overloading the email server or hitting provider API limits. This might mean processing e.g. 100 per minute (depending on limits) or similar. The user doesn’t control this but should be aware that for very large campaigns it might take some time for all to go out. Possibly indicate in UI if a bulk send is still in progress and how many done. This is more technical, but functionally, ensure reliable delivery even for high volume by queuing.

- **FR 3.2.9 Error Handling in Sending:** If something goes wrong during the sending process, the system shall handle it gracefully:

  - If the reward provider’s API fails to return a code (e.g., service down), the system should retry a few times. If still failing, mark those sends as “Pending” or “Failed” and notify an admin to intervene. The user who initiated might get a warning “Some rewards could not be fetched at this time; they will be retried automatically.” And in tracking, they appear as pending fulfillment.
  - If email sending fails for a particular recipient (e.g., invalid address or SMTP error), mark that reward as “Undeliverable” and surface it so the user can possibly correct the address and resend (functionality to resend is needed in tracking section).
  - The system must ensure that any error does not crash the whole bulk process. It should isolate and continue with other recipients.
  - If a scheduled send fails to go out at the right time (say due to server downtime), the system should send it as soon as possible when back up, and there should be a mechanism to catch up on missed scheduled tasks.

- **FR 3.2.10 Storing Delivery Info:** For each reward issuance, the system shall store the details of that "transaction": who sent it (user id), when, which reward (catalog item reference), which recipient (at least email or identifier), any message included, the send method (email/SMS), and any ID/reference from the provider (like the code or an order ID from gift card vendor). This data is crucial for tracking, support, and audit. It should be stored securely, especially the code should be stored in a safe way (perhaps encrypted if we keep it, or at least not in plain text accessible to all). This ties to security (protect the actual voucher codes from unauthorized access).

- **FR 3.2.11 Support for Multi-Reward Bundles (Optional):** In some cases, a user might want to send a choice of rewards to a recipient (i.e., the recipient can pick one of several). If the platform supports this (which is a nice feature to increase recipient satisfaction), then in the sending workflow, the user would pick multiple reward items (e.g., “Offer either a $50 Amazon card or a $50 Starbucks card”) and send as one “bundle”. The recipient would get a single link, which leads to a page where they choose one of the options. Once they choose, the others become invalid. This is an advanced scenario, but if we plan it:
  - The system shall allow selection of multiple rewards as alternatives, up to a reasonable number (maybe 3-5 options).
  - It shall ensure only one is redeemed (the redemption workflow would handle locking out the others once one is taken).
  - For budgeting, perhaps count the cost of the one actually redeemed (if pre-charge, might hold the highest cost or average, but that complicates budgets – likely treat as if the one chosen was the one spent).
  - This feature’s requirements would reflect in redemption section as well. For now, it’s optional and flagged as future/advanced.

In summary, the Reward Delivery feature must make it easy for authorized users to deliver rewards reliably and flexibly, whether one by one or at scale, now or later, with personalized communications, while interfacing correctly with the underlying reward providers and communication channels. The success of this feature is judged by how intuitive the sending process is and how reliably recipients actually receive their rewards.

### 3.3 Reward Tracking and Lifecycle Management

**Description:** After rewards are sent, the platform will provide tools to track their status throughout the lifecycle (from creation to final redemption or closure). This feature is crucial for transparency and program management — product managers need to know which rewards have been claimed and which are still pending, and finance teams need to know which have been used (to account for actual expenses). Lifecycle tracking also helps identify issues (like failed deliveries or unredeemed rewards that might need reminders or follow-up).

The typical statuses a reward might go through include: _Initiated/Sent_, _Delivered_ (if we get confirmation of delivery, e.g., email delivered), _Opened_ (if we track that the email was opened or link clicked), _Redeemed_, _Expired_, _Cancelled_, _Failed_. Not all statuses apply to all scenarios (for example, “Delivered” could be ambiguous for email, but we can treat sending as delivered unless bounced). The system should present these statuses clearly to users and allow filtering and reporting by status.

Additionally, tracking involves enabling certain actions on rewards post-send, like resending an email, canceling a pending reward (if possible), or manually marking something if needed.

**Functional Requirements:**

- **FR 3.3.1 Reward Status Tracking:** The system shall maintain a **status for each reward instance** (each reward sent to a specific recipient) and update it as it moves through the lifecycle. The statuses should include at least the following:

  - **Sent/Pending Delivery:** The reward has been created in the system and an attempt to deliver (email/SMS) has been made. This might be the initial status immediately after sending action if we don’t yet know delivery outcome.
  - **Delivered:** Confirmation that the reward notification reached the recipient. For email, “delivered” could mean we got a success response from email server (i.e., not bounced). For SMS, delivered receipt from SMS gateway. This status might be skipped if we consider “Sent” as good enough. However, tracking bounces is important: if email bounce occurs, perhaps a status **Undeliverable** or **Failed Delivery** is set.
  - **Opened:** If the platform includes tracking pixels in emails or unique link clicks, it can mark a reward as “Opened” when the recipient views the email or clicks the redemption link. This indicates the recipient is aware of the reward. This status might be optional if tracking is available; not all use cases need it.
  - **Redeemed:** The ultimate success state. The reward has been redeemed by the recipient. For digital codes, redeemed means the recipient took the code and presumably used it (though platform might not always know if the code was actually used at the merchant; often we mark redeemed when we display the code to the user or when they click a “Redeem” button on our page). For physical items, redeemed could mean the recipient confirmed their shipping address (i.e., accepted the gift) or the item was delivered to them. We must define triggers for marking redeemed: it could be user clicking a "Claim" button, or integration with provider telling us code used, etc. The system shall update to Redeemed at the appropriate trigger and timestamp it.
  - **Expired:** If a reward remains unredeemed beyond a certain period or has an inherent expiration (some gift cards might expire, or we set an expiration for claiming the reward code), the system shall mark it as Expired. Expired means the recipient can no longer claim it (maybe the code is withdrawn or donation is returned). Expiration rules should be configurable per reward or campaign (e.g., “this reward offer expires in 3 months if not claimed”). If expired, if the code was not used, possibly it could be reclaimed or reused (that ties to budget reclaim features if any).
  - **Cancelled:** If an admin/user proactively cancels a reward after sending but before redemption (for example, they sent in error to wrong person and want to invalidate it), the system can mark it as Cancelled. If the reward was not yet redeemed, cancellation means the code is invalidated (if possible via provider; some providers allow cancellation of unused gift card codes for a refund). If not possible to invalidate, then cancellation just notes it and prevents redemption through our portal (but if code was delivered, this is tricky – better to not allow cancellation after code delivered unless we can confirm it's unused and block it via provider).
  - **Failed:** If something in the process failed irrecoverably. E.g., if generating the gift card code failed and after retries it never completed, the reward might be marked as Failed, and essentially it was never successfully sent. Or if a physical shipment failed (item lost and can't be fulfilled). These cases might need manual intervention. The system should surface failures clearly for action.
  - **Pending Approval:** (If we introduce approvals for rewards over certain budget, a reward could be in pending state waiting for manager approval – but this is an additional complexity not explicitly asked, so we might skip detailed. If needed, mention under budgets or RBAC that expensive rewards might require approval, meaning a status before Sent like “Pending Approval”.)

  The system shall present these statuses consistently in the UI and use icons or labels to make them easy to identify.

- **FR 3.3.2 Reward Dashboard/List:** The system shall provide a **Rewards Tracking Dashboard or List View** for users to monitor all rewards they have sent (or that their organization has sent, depending on permission). This could be under a “Sent Rewards” section showing a table of rewards with columns like Recipient, Reward, Value, Date Sent, Status, Date Redeemed (if applicable). Users should be able to filter this list by campaign, by status, by date range, by sender (if an admin overseeing multiple senders), and by recipient (search by email or name). For instance, a product manager can filter “show me all rewards I sent in Q1 and see how many are redeemed vs pending.” An admin might filter “show all rewards in the system that are still pending after 3 months”.

- **FR 3.3.3 Status Updates:** The system shall **automatically update statuses** based on events:

  - If an email bounces, mark as Undeliverable (and maybe notify the sender or mark attention).
  - If a recipient clicks the redemption link, mark as Redeemed (or at least as Claimed, and then perhaps final redeemed if they complete any subsequent steps).
  - If using certain gift card APIs that allow checking if a code was redeemed, the system can periodically update whether a code was used at the merchant (though often not feasible in real-time).
  - If a physical gift was shipped, integration might update “Delivered” once shipment tracking says delivered.
  - Many of these rely on integration events or periodic checks. The system should incorporate a mechanism (like webhooks from providers or scheduled tasks) to refresh reward status. For example, for each unredeemed reward, maybe check daily via API if it's been redeemed (if provider supports querying code status).
  - For statuses purely internal, like if user redeems on our site, we update immediately.

- **FR 3.3.4 Manual Status Override:** The system shall allow authorized users (likely Org Admin or Program Manager in some cases) to **manually adjust the status** of a reward in case of discrepancies. Example: If a reward was given via an external method (like they gave the code in person) and they want to mark it as redeemed in the system for completeness, they should be able to. Or if a redemption happened offline, the admin can mark it. Manual override should be logged (audit) and possibly restricted (maybe only Admin role).

  - Not all statuses should be manual – you probably can mark something as redeemed or cancel something, but not arbitrarily; perhaps a user can “force expire” or “cancel” a pending reward.
  - If a user marks something as cancelled that was already delivered, system should warn about consequences (like “if the recipient already has the code, you should inform them it's cancelled; the code might still be usable if they try unless invalidated with provider”).

- **FR 3.3.5 Resending and Reminders:** For rewards in certain statuses, the system shall offer actions:

  - If a reward is **Undeliverable** (email bounced), allow the user to edit the email address and **resend** the reward. The system would then attempt delivery again (possibly generating a new link if needed, or same link if still valid).
  - If a reward is **Pending (Not Redeemed) for a long time**, allow the user to **send a reminder** email to the recipient. This could be manual (user clicks “Resend Reminder”) or automated (system triggers a reminder after X days if not redeemed, if configured). The reminder essentially re-sends the redemption link with perhaps a different template (“Friendly reminder: you have a reward waiting!”).
  - If a reward is **Scheduled** (future send) and not yet sent, allow user to cancel or edit the schedule.
  - The UI should clearly show available actions for a selected reward based on its status (e.g., a “Resend Email” button for Undeliverable or “Send Reminder” for Unredeemed after some days, “Cancel” for scheduled or maybe for not-yet-redeemed to invalidate it).

- **FR 3.3.6 Reward Details View:** Users should be able to click on a specific reward entry to see a **detailed view** of that reward’s history. This would show information like: Who sent it and when, full recipient details, message sent, the code or redemption link (possibly partially masked for security), current status, and a timeline of status changes (e.g., “Sent on Jan 1, Opened on Jan 2, Redeemed on Jan 5”). It should also log if any reminders were sent or any manual changes made (with timestamps and user who did it). This acts like an audit trail for that reward instance, useful for support queries like “I didn't receive my gift” – the admin can look and see it was sent and opened, etc.

- **FR 3.3.7 Aggregated Tracking:** The platform shall provide some aggregate tracking views, such as:

  - “X of Y rewards in this campaign have been redeemed (Z% redemption rate)”. This kind of summary might appear in a campaign overview or the dashboard. It’s more in reporting, but it’s tied to these statuses.
  - For each campaign or distribution, show summary counts: Sent, Redeemed, Pending, etc.
  - Possibly show charts or progress bars for visual management.

- **FR 3.3.8 Integration with Budget:** When a reward is redeemed or expired, it might affect budget accounting. For example, if budgets are counted on redemption instead of send, the system needs to update that. (We will clarify in budget section, but tracking ties in: if we only count cost at redemption, then until redeemed, it’s a liability but not an expense. The system should be able to report both distributed vs redeemed cost.)

  - Possibly track an attribute “Cost incurred” – which could be at send or redemption depending on client’s accounting preference.

- **FR 3.3.9 Data Retention of Rewards:** For compliance, the system might not keep personal data indefinitely. Maybe after a certain period post redemption/expiration, personal info might be anonymized. But at least for active and recent rewards, tracking data stays. (We might mention data retention under compliance, but it affects how long we see details here. E.g., after 2 years, maybe only aggregated data remains, etc.)

To illustrate typical status progression, consider an example: A reward is sent via email – it starts as **Sent**. If the email bounces, it goes to **Undeliverable**; if not, it remains in Sent. The recipient opens the email and clicks the link – system marks **Redeemed** (assuming clicking claim equals redeemed). If they never click and the reward code expires after 3 months, system marks **Expired**. At any point before redemption, the admin could **Cancel** it (which if done, they should ideally inform the recipient if they had gotten the email, or the redemption link should show “this reward is no longer available”).

The platform must manage these transitions systematically:

**Table 3.3 - Reward Lifecycle Statuses:** (Summary of statuses and their meaning)

| **Status**        | **Meaning**                                                                                                                                                                       | **Possible Next States**                                                                                               |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Sent**          | Reward has been sent (email/SMS dispatched) or is in the process of being delivered. Default state after user initiates send.                                                     | Delivered, Opened, Redeemed, Undeliverable (if bounce), Expired (if time passes without action), Cancelled             |
| **Delivered**     | Delivery confirmed (e.g., email did not bounce). _Optional explicit state; if not distinguished, assume Sent implies delivered._                                                  | Opened, Redeemed, Expired                                                                                              |
| **Opened**        | Recipient opened the reward notification (email open or link click detected). Indicates engagement but not yet redeemed.                                                          | Redeemed, Expired                                                                                                      |
| **Redeemed**      | Recipient has redeemed/claimed the reward. This is a terminal success state.                                                                                                      | (No further states; possibly could go to Cancelled if we revoke, but normally once redeemed it's final)                |
| **Undeliverable** | The reward could not be delivered to recipient (e.g., invalid email address or SMS failed). User intervention needed.                                                             | (After correction) Sent (retrial), or Cancelled                                                                        |
| **Cancelled**     | The reward was canceled by an admin before redemption. The code is void (or should not be used). Terminal state (though possibly could be re-sent as new if needed).              | (No next state; considered closed)                                                                                     |
| **Expired**       | The reward offer expired before being redeemed. Recipient can no longer claim it (link/code disabled if possible). Terminal state.                                                | (No next state; considered closed, though potentially admin might issue a replacement, which is a new reward instance) |
| **Failed**        | An error occurred in creation or delivery and the reward could not be issued (distinct from undeliverable). E.g., provider failure. Needs user/admin to possibly retry or cancel. | Sent (if retried), or Cancelled                                                                                        |

_Table 3.3_ – Reward lifecycle statuses and transitions. This lifecycle is managed by the system automatically, with manual overrides where appropriate. Not every implementation will explicitly use all states (for example, some systems might just have Sent and Redeemed), but our platform aims for granular tracking for maximum insight.

- **FR 3.3.10 Dashboard Alerts for Outstanding Items:** The system shall highlight important tracking information on the dashboard or via notifications. For instance:
  - Alert if there are any undeliverable rewards needing attention (“5 rewards failed to send – click here to review”).
  - Summary of unredeemed rewards that are nearing expiration (“10 rewards will expire next week, consider sending reminders”).
  - This ensures timely management of the reward lifecycle by the user.

Through these tracking features, IncentiveHub will give product managers and admins peace of mind and control: they can always know the status of the incentives they sent out, take actions if needed, and report on outcomes effectively.

### 3.4 Reward Redemption Process and Recipient Experience

**Description:** The Reward Redemption process refers to how recipients (employees, customers, partners, etc.) actually claim and use the rewards they've been sent. This involves the user experience on the recipient side, such as receiving an email or text, clicking a link, and being guided through obtaining their reward (like seeing a gift card code or confirming shipping for a physical item). Ensuring a smooth and simple redemption process is critical, as it directly impacts the satisfaction of the end recipients and the credibility of the reward program.

This section covers the requirements for what happens from the moment a recipient is notified of their reward to the point where they successfully redeem it. It also covers error handling from the recipient’s perspective (like what if the link doesn't work or they have questions) and how the system handles redemption in various scenarios.

**Functional Requirements:**

- **FR 3.4.1 Reward Notification to Recipient:** When a reward is sent, the system generates a **notification to the recipient**. This will typically be an email (or SMS, etc.), formatted in a clear and appealing way. Requirements for the notification:

  - It shall include the sender’s name or organization (e.g., “From: Acme Corp Rewards Program” or if personal, “John Doe via IncentiveHub” depending on how we set sender name) so that the recipient recognizes who the reward is from.
  - It shall include a concise message or the personal note from the sender, explaining why they are receiving the reward (if provided by sender).
  - It shall clearly state what the reward is (e.g., “You’ve received a $50 Gift Card!” possibly with the brand logo).
  - Importantly, it shall include a prominent **call-to-action**: e.g., a button “Claim Your Reward” or “Redeem Now”. This button or link will direct the recipient to the redemption page.
  - If the reward is something that can be directly delivered in the email (like a generic coupon code), we might include it in the email body itself along with instructions. However, generally using a link is safer for tracking and flexibility.
  - The email should also include any necessary information like expiration date of the reward or any terms (“This gift card expires on ...” or “Use code at checkout” if embedded).
  - Branding: The email template should be customizable with the company's branding (logo, colors) so it feels like it came from the company, not a random platform (this will likely be configurable by Org Admin).
  - Support contact: The notification should provide a way for the recipient to get help if needed (e.g., a line “Questions? Contact support@yourcompany.com” or a link to FAQ). Likely this is the sending company’s support or a platform support depending on configuration.

- **FR 3.4.2 Secure Redemption Link:** The redemption link or button provided to the recipient shall be a **secure, unique link** that directs to a redemption page hosted by the platform. Requirements:

  - The link should contain a secure token so that only someone with the link can access the reward details (a long random identifier, not guessable).
  - The link ideally should be one-time use or bound to that reward; if someone tries to reuse it after redemption, it should not show the reward again (should indicate already redeemed).
  - The link should use HTTPS and perhaps be short enough if SMS usage (maybe a short URL domain if via SMS).
  - When the recipient clicks the link, they may be asked to confirm their identity in some cases. Since recipients might not have accounts on the platform, typically the link itself is the authentication (the token serves as proof). If extra security is needed (for instance, employee rewards might optionally require them to log in with corporate account to claim, to prevent someone else intercepting their email), the system should allow the sender to require login. But default is no login, just the link (for ease, especially for external recipients).
  - The redemption page will use this token to fetch the relevant reward details and show appropriate content.

- **FR 3.4.3 Redemption Web Page:** The system shall present a **Redemption Page** to the recipient when they follow the link. This page’s content will depend on the type of reward:

  - For a **digital gift card or code**: The page should greet the recipient (maybe with their name if known, e.g., from how the sender filled it out) and display the gift card code or redemption instructions. Often, such pages might have a “Click to reveal your code” for an extra step (some systems hide the code until clicked, possibly for tracking that action as redemption). Once revealed, it could show “Your code: ABC123. Use this on the retailer’s site.” Possibly also provide a convenient button like “Redeem on Amazon” which goes to Amazon’s redeem page if known.
  - For a **physical item**: The page might say “You have been awarded [Item]. Please provide your shipping address to receive this gift.” There would be a form for the recipient to enter their preferred shipping address (and possibly phone number for delivery) if the sender didn’t already specify an address. The system should validate the address (maybe integration with an address validation API if available, or at least ensure required fields). After submission, it might show confirmation “Your address has been received. Your gift will be shipped within X days.” and mark the reward as redeemed/claimed in our system. This info should be sent to the fulfillment partner to dispatch the item.
  - For **choice of rewards scenario** (if multiple options were offered via one link): The page would present multiple choices: e.g., “Choose your reward: (A) $50 Amazon Card or (B) $50 Starbucks Card.” The recipient selects one and clicks redeem. The system then displays/redeems the chosen one and confirms the choice. The others become unavailable afterward.
  - For **coupon/promo code**: The page might directly show the code and maybe usage instructions or link to where to apply it.
  - For **charity donation**: The page might say “A donation of $X to [Charity] will be made in your name. Click confirm to accept.” Or possibly let them choose a charity among options if that was the design.

  In all cases, the page should be simple, mobile-friendly, and contain contextual instructions. It should also have branding of the sending organization (if configured), and possibly the platform branding discreetly (“Powered by IncentiveHub” or so, if allowed by client).

  Additionally, after redemption action, the page should display a **confirmation** or thank-you message. For example, “Thank you! Your gift card code is shown above. It has also been emailed to you for convenience.” or “Thank you! Your selection has been recorded. You will receive your gift soon.” Possibly include contact info for support, and maybe some engagement (like if it's a customer reward, maybe a link back to the company’s site or a promotional message, but that might be up to the sender customizing the page content.)

- **FR 3.4.4 Redemption without Email (Alternate Flows):** In some use cases like a live event or in-app reward, a recipient might get a reward link through another channel (like displayed on screen or via a direct app message). The system should allow redemption via that link just the same. Also, if a recipient loses the email, the sender should be able to resend it (covered prior) or retrieve the redemption link to share with them manually. The platform might provide a “Copy redemption link” function to admins for each reward.

- **FR 3.4.5 Error Handling on Redemption:** The system shall handle common errors a recipient might encounter:
  - **Invalid or Expired Link:** If a recipient clicks a link that’s invalid (e.g., token mistyped or expired), the redemption page should show a clear error message: “This reward link is invalid or has expired. If you believe this is a mistake, please contact the sender or support.”
  - **Already Redeemed:** If the link was already used, the page should inform the user: “This reward has already been redeemed.” If possible, maybe show when (e.g., “redeemed on Date by [maybe their own email]”) – but likely just say already redeemed and to contact if they think they haven’t (meaning maybe someone else used it if forwarded).
  - **Technical issues:** If the server has an issue retrieving reward details, show a generic “We’re sorry, something went wrong. Please try again later or contact support.” (And log the error internally).
  - **Partial redemption flow issues:** e.g., if address submission fails validation, show errors for fields. If the chosen reward in a multi-choice scenario is out of stock (shouldn’t happen if we reserved them properly, but if so), inform them and possibly allow them to pick another.
  - The redemption page should be robust against multiple submissions (like if user refreshes or clicks twice, ensure not double redeem etc.). Possibly by having the backend check status and not issuing two codes.
- **FR 3.4.6 Guidance and Support for Recipients:** Recognizing that recipients might not be familiar with the platform, the system shall provide guidance:
  - On the redemption page or in the email, include a brief explanation: e.g., “What is this? You’ve been sent a reward through [Company Name]’s reward system as a thank-you. Follow the instructions to claim it. This is a legitimate reward, not spam.” (Many recipients might be wary of scam emails, so including the context is crucial).
  - Provide a **support link**: possibly a small “Help” or FAQ link on the redemption page that opens info on common questions: “Is this legit? How do I use my gift card? What if I lost the email? What if I have trouble?” – these could be answered in an FAQ. We might provide a default platform FAQ, but ideally it’s branded for the company. At minimum, a contact email/phone for support (which likely goes to the company’s rewards program manager or a generic support).
  - Accessibility for recipients: the redemption page should be accessible (for disabled users), as per WCAG guidelines (e.g., screen-reader friendly for blind users who get an email and need to redeem).
- **FR 3.4.7 Redemption Confirmation to Sender (optional):** The system could notify the sender when a reward they sent has been redeemed (if they opted for such notification). For example, a product manager might get an email: “Your reward to jane.doe@example.com has been redeemed on 2025-05-01.” This might be a setting whether they want those notifications or just check the dashboard. But this keeps them in the loop.

- **FR 3.4.8 One-Click Redemption (if applicable):** For certain simple rewards, the email itself might carry enough info that clicking is not even needed. For example, “Your coupon code: XYA12 – use at checkout.” In such cases, we treat showing the email as effectively delivered the reward. But if we want a track of redemption, might not mark redeemed until they actually use it (which we might not know). It's tricky, so we likely keep the flow that clicking the link is needed for redemption so we can mark redeemed.
  - However, for internal employee gift where every employee gets something by default, maybe there is no action needed by them, except just enjoy it. But even then, likely there's an acknowledgment step.
- **FR 3.4.9 Multi-Factor for High-Value Rewards (optional security):** If a reward is of very high value or sensitive (like a large sum or something, or maybe a sensitive survey incentive requiring anonymity), an additional verification step might be needed. For example, for an anonymous survey, they might not want to collect email but provide a code at survey end; the redemption link might ask the user to enter a reference number from the survey (to link their response) – though truly anonymous means no linking, so maybe skip that scenario. Or for high-value, maybe an OTP to their phone to verify identity before showing a $1000 gift code. This is probably overkill for general use, but we mention possibility for completeness. The default assumption: the link in their email is sufficient security.

- **FR 3.4.10 Localization of Recipient Experience:** If the platform supports multiple languages, the redemption page and notification should ideally appear in the recipient’s language. If the sender knows the recipient’s preferred language (maybe input or based on domain or separate field), they could select the email template language. Or the system might detect the browser language on redemption page. At least, allow the content to be translated (the fixed strings, not necessarily the custom message from sender). E.g., “Claim your reward” button could be in French if the user is French. We cover localization more later, but just to note, recipient side should be localized too.

- **FR 3.4.11 Provider Integration on Redemption:** The system will sometimes need to interact with the reward provider during redemption. For instance:

  - If a gift card provider provides a redemption URL, maybe our link directly goes to their site (some systems just send a link to the provider’s gift portal). However, we likely present ourselves.
  - If a provider requires activation or confirmation: e.g., some prepaid cards might need activation after user gets it. The system might call an API at redemption time to activate the card for use.
  - Physical fulfillment: when user enters address, our system must send that to fulfillment partner’s system (via API or file) to initiate shipping.
  - If the reward was not pre-fetched, on clicking redeem, the system might in real-time request a code from provider to show (some designs choose to only fetch the code when user actually goes to claim, to avoid wasted codes for those who never open). That’s fine as long as it’s quick. If the provider call fails at that moment, we need an error: “Sorry, we are having trouble retrieving your reward, please try again in a bit.” And keep it pending.
  - Thus, redemption process might involve some back-end transactions, which should ideally be invisible to user aside from a possible short loading spinner.

- **FR 3.4.12 Post-Redemption Usage (Out of Scope for Platform but context):** Once redeemed, the user now has a gift card code or item. Using it (like spending the gift card at the retailer) is beyond our platform’s scope. We just consider it done. If they encounter issues using at retailer, they would contact that retailer or the original sender; our platform might not have info. However, if the code was invalid or already used (rare if new), that is something platform should handle as a support issue with provider. Possibly, an admin could issue a new code if one turned out invalid.

- **FR 3.4.13 Data Capture on Redemption:** Any data input by recipient (like address, or choosing an option) should be captured and stored linked to that reward record for reference. Possibly visible to the sender in the reward details (so they know where the item is being shipped, etc.). This data is sensitive (address is personal data) and should be protected & used only for fulfillment and then possibly deleted after use per privacy policy.

**Recipient Journey Example:** _(To illustrate the flow from a recipient’s perspective, non-normative)_

- John, an employee, receives an email from “ACME Corp Rewards” with subject “You’ve received a reward!”. He opens it and sees a message from his manager thanking him for his work and indicating there’s a $50 Amazon gift card attached. He clicks the “Claim your $50 Amazon Gift Card” button.
- His web browser opens a page on rewards.acmecorp.com (branded subdomain perhaps) showing ACME logo and “Hi John, you have a $50 Amazon Gift Card.” He clicks “Reveal Code” and the page displays the code “XYZ123456” and a link to Amazon’s redemption page. It also says “Copy Code” which he uses to copy it, and an instruction “Use this code at amazon.com to add $50 to your account.”
- The system records this as redeemed. John also gets a follow-up email confirmation from the platform: “Your $50 Amazon Card code: XYZ123456. Keep it for your records.”
- If John had any issue (say code didn’t work), he could reach out via a link in the email that says “Contact rewards support at hr@acmecorp.com”.
- Alternatively, if John never clicked the email for a week, he might get an automated reminder or his manager might manually remind him. If a month passed and ACME set 1 month expiration, the link might then show “expired” and John would have to ask if it can be reissued.

**Error Case Example:**

- Jane, a customer of ACME, gets a reward offer email for a $20 voucher because she referred a friend. She deletes it thinking it’s spam. The ACME product manager sees in the system that Jane’s reward is unredeemed after 2 weeks. They click “Resend” which sends another email. Jane this time clicks and redeems it.
- If Jane had clicked after it expired, she might see “expired”. She contacts support; the product manager, feeling generous, can issue a new reward (they’d create a new one for her manually since the old one is expired).

By meeting these redemption requirements, the platform ensures that receiving a reward is a delightful and hassle-free experience for the end user, which in turn makes the incentive program effective (a frustrated user who cannot redeem a reward might actually turn negative toward the program, which we want to avoid at all costs).

### 3.5 Budget Management

**Description:** Budget Management features enable organizations to control and monitor how much is being spent on rewards. Since incentives often come from a marketing or HR budget, it’s crucial to set limits (so you don’t overspend) and track spending in real time. The platform will allow admins or finance roles to define budgets for specific scopes (e.g., an annual budget for the whole company’s rewards, or separate budgets per team, campaign, or manager) and then track all rewards against those budgets. It will enforce rules like preventing sends that would exceed the budget or requiring approvals for over-budget actions.

The budget module also includes the ability to view remaining funds, see breakdowns of spending, and adjust budgets. Integration with reporting is strong here, as well as possibly integration with finance systems if needed (but likely just exports). It might also manage how the funding is supplied (e.g., if the company pre-purchases credits). However, internal financial transactions might be out of main scope beyond tracking usage; the focus is giving the user a clear understanding of how much they've spent and can still spend on rewards.

**Functional Requirements:**

- **FR 3.5.1 Define Budgets:** The system shall allow authorized users (e.g., Org Admin or Finance Manager roles) to **create and configure budgets** for reward programs. Key elements to define:
  - A **Budget Name/Label** (e.g., “2025 Employee Rewards Budget” or “Q1 Customer Referral Campaign Budget”).
  - A **Time Period** (optional) – budgets could be ongoing or tied to a date range. For example, a yearly budget resets each year, or a campaign budget is only for the campaign duration. If time-bound, specify start and end dates. If not, it’s just a static pool until changed.
  - A **Budget Amount/Limit** – the monetary amount allocated. This might be in the organization’s base currency (say USD) or a specified currency for that budget. If multi-currency rewards are allowed, how to count them against the budget? Likely everything converts to a base currency for counting. So if someone sends a €50 reward and base is USD, it might count ~$55 towards budget (using a consistent conversion rate, maybe at transaction time).
  - **Scope**: The budget could apply globally (to all rewards sent by the org) or to specific subsets:
    - by **User or Role**: e.g., each product manager can have a personal budget they cannot exceed (the admin assigns each manager a budget limit).
    - by **Team/Department**: maybe using tags or grouping of users.
    - by **Campaign**: if the platform has campaign concept (maybe grouping of related reward sends), a budget can be assigned to that campaign.
    - The system should support at least one level (global vs maybe per campaign). For initial scope, we might implement a primary global budget plus optional campaign budgets as needed. As an example, an Org Admin might set an overall cap (like $100k for year), and also within that, allocate $30k for referrals, $50k for customer loyalty, $20k for research incentives. This implies multiple budgets can co-exist and a given reward might need to be linked to one of them.
  - **Currency**: If budgets can be in different currencies, this complicates matters. Perhaps simpler: define a base currency per org (like at onboarding, they choose USD or EUR). All budgets and reports are in that currency; if rewards in other currency, convert at time of sending to count. We’ll assume that approach unless multi-currency budgets is a must. Possibly allow separate budgets by region in local currency if needed.
- **FR 3.5.2 Associate Rewards/Campaigns with Budget:** The system shall ensure that every reward send is associated with a particular budget for tracking. If only one global budget exists, all go there by default. If multiple budgets exist, when a user initiates sending a reward, the system should determine which budget to apply:

  - Possibly by context: if user has only one budget they’re allowed, automatically use that.
  - If multiple apply (like multiple campaign budgets open), let the user choose which budget this should draw from (maybe a dropdown “Select budget” if they have access to more than one).
  - We might implement “campaigns” as an entity where a campaign has a budget attached and all rewards under that campaign count to it, which might streamline selection (the user might first select which campaign or program they’re sending under).
  - The association is then stored so the spending goes to that budget. Also, if budgets are hierarchical (like multiple sub-budgets summing to a master), the system needs to propagate if needed.

- **FR 3.5.3 Real-Time Budget Checking:** Whenever a user attempts to send a reward (single or bulk), the system shall perform a **budget check**:

  - Calculate the total cost of the planned send (sum of values of all rewards to be sent).
  - Check against the remaining budget of the relevant budget allocation.
  - If the cost would exceed the remaining budget, the system should enforce one of the following based on configuration:
    - **Prevent** the action outright: show an error “Insufficient budget. You only have $200 remaining and this action costs $250. Please request a budget increase or adjust the reward.”
    - **Warn and require override/approval**: e.g., allow the user to submit the request for approval by an admin or finance (i.e., an approval workflow). The SRS didn't explicitly require an approval workflow, but it’s a natural extension. Possibly we say if user lacks permission to overspend, they cannot send; an admin could override by increasing budget or approving.
    - Or if the user has permission to overspend (maybe admin role), either let them or still warn.
  - This ensures budgets are respected. The threshold for warning could also be configurable (like warn at 90% usage even if not over).
  - For bulk sends, if partially over, you might have to trim list or increase budget; splitting isn't automatic unless perhaps sending the portion that fits, but that would be odd, so likely all or nothing with a clear message.

- **FR 3.5.4 Budget Deduction Accounting:** The system shall deduct from the budget when rewards are sent (or when redeemed, depending on the accounting mode configured).
  - **Accounting Mode**: There are two common ways:
    1. Deduct upon sending (authorization) – the moment you send a $50 reward, treat $50 as spent. If the reward is later not redeemed and can be refunded or never actually used, that could free up budget but often budgets treat it as spent regardless (unless reclaiming unused funds is a thing).
    2. Deduct upon redemption – only count if the person actually claims it, so unclaimed rewards don’t count as spent. This is beneficial if using “pay on redemption” model with providers, so you only pay for what’s used.
  - Our platform should ideally support both approaches because different companies might prefer one method. As a default, we can use “deduct on send” for simplicity (ensures you don’t accidentally promise more than you budgeted), and then if a reward expires unredeemed, possibly the admin can manually credit back or reuse.
  - We should document how we handle it:
    - If _Deduct on Send_: every send reduces available budget. If some rewards expire or are canceled, the system could either automatically credit back (increase remaining budget) if it knows no cost was incurred, or provide a manual adjustment. Perhaps simpler: budgets are consumption-based, only manual adjustments if needed.
    - If _Deduct on Redemption_: the system might “hold” the amount until redeemed. For example, mark it as “allocated” vs “spent”. So show both allocated and actually spent. If not redeemed by expiry, release it.
  - Possibly simpler approach: track two numbers: Distributed (sent) and Redeemed. Then an admin can see “we allocated $10k, but only $8k redeemed, so effectively $2k was not utilized”. But the budget consumption could consider distributed as spent for planning, with the understanding not all gets used.
  - For our requirements: The system shall decrement the remaining budget immediately when a reward is sent (ensuring it never goes negative), and if that reward later expires or is canceled prior to redemption, the system **may** add it back to the remaining budget (especially if in same budget period). We’ll allow that logic, as it makes sense to free up funds from unused rewards.
- **FR 3.5.5 Budget Dashboard:** The system shall provide a **Budget dashboard or summary screen** for finance/admin users. This would show:
  - List of all active budgets with their total amount, amount spent (and/or committed), remaining amount, and possibly percentage used, and time period.
  - Visual indicators like a bar showing usage.
  - If multiple budgets: allow drilling down. E.g., click a budget to see details: transactions (each reward or batch with cost), which users or campaigns consumed what.
  - If applicable, show forecast or trends (maybe out of scope for now, but could be “at this rate you’ll exhaust in 2 months”).
  - Also highlight any budgets that are close to limit or overused.
  - Possibly show separate columns for redeemed vs sent usage if tracking that difference.
- **FR 3.5.6 Budget Modification:** Authorized users shall be able to **adjust budgets** as needed:
  - Increase or decrease the limit (with logs to audit who changed it and when, as this could be sensitive).
  - Extend a time period or close a budget early.
  - Create new budgets or retire old ones (closing a budget might disallow further use and maybe move remaining funds to another if needed).
  - If budget period ended but some rewards still pending redemption, decisions: likely those were counted already, and if redeemed after period, still counted in that period’s results. Might not allow sending after end date though.
- **FR 3.5.7 Multi-level Budgets (optional):** In some cases, budgets might roll up in a hierarchy. For example, each department has a budget, and there’s a company-wide budget that is sum of all. This might be advanced to implement. We might skip detailed handling but allow it conceptually:
  - Possibly implement parent-child budgets. If a child goes over, maybe parent can cover.
  - This is probably beyond initial scope, so mention as future capability.
- **FR 3.5.8 Approvals (optional workflow):** If an organization wants oversight, the system shall support an **approval workflow** for certain budget-related actions:
  - If a user tries to send a reward above a threshold or that causes budget exceed, instead of outright preventing, the system could create a “pending approval” request for a manager. The manager (or admin) gets a notification and can approve or deny. If approved, the send proceeds (maybe automatically completes sending or user has to re-trigger).
  - This can also apply to budget increases: a manager could request a budget top-up and an admin approves it.
  - For the SRS, we can note: _Optionally, the platform can enforce an approval for any reward that exceeds a configurable amount (e.g., any single reward over $1000 requires CFO approval) or if budget is insufficient. This ensures large expenses are overseen._
  - Implementation: might be easier to just prevent and require manual budget increase by admin. But it's an enterprise feature that might be asked.
- **FR 3.5.9 Notifications and Alerts (Budget):** The system shall provide notifications related to budgets:
  - If a budget is running low (e.g., falls below 10% remaining), notify the budget owner or admin (“Alert: Only $500 left in Q4 Rewards Budget”).
  - If a send was blocked due to budget, notify admin maybe that someone attempted and failed due to budget (so they can follow up).
  - If an overspend is allowed and happens, definitely notify admin (“Budget exceeded by $X by user Y”).
  - If budgets reset periodically, send summary at period end (“You used 85% of Q1 budget”).
  - These notifications can be in-app or email to relevant roles.
- **FR 3.5.10 Reporting Integration:** The budget usage data shall be available in reports (see Reporting section). E.g., one should be able to produce a report per budget or overall that shows how funds were spent, maybe broken down by category or by time.
  - Could have a monthly report of spending vs budget.
  - Possibly export for finance reconciliation: list of all reward transactions with their amounts (like an expense ledger).
- **FR 3.5.11 Handling Multiple Currencies:** If an organization sends rewards in multiple currencies (e.g., sends some USD gift cards and some in EUR), how does budget reflect that? Approaches:
  - All budgets in a single currency (org base). Convert others to base when counting. The system should use a consistent conversion rate (maybe updated daily or fixed at time of send) to calculate the budget impact. We should note potential exchange rate differences (maybe negligible for internal tracking, but if currency fluctuates, actual cost could differ if paying provider in local currency).
  - Alternatively, maintain sub-budgets per currency. But likely stick to one currency.
  - We'll say: **The system shall support currency conversion for budget accounting.** If a reward in a different currency is sent, the system will convert its value to the budget’s currency using a predetermined exchange rate (e.g., from a reliable source updated periodically) and count that amount against the budget. For consistency, possibly capture the rate used each time to not retroactively change things if rates change.
- **FR 3.5.12 Funding Mechanism (Informational):** While the platform tracks budgets, how the actual money flows might be abstracted:
  - The platform may require the organization to pre-pay or have a credit balance. If so, budget could be tied to that balance. For instance, a company deposits $10k, which is the budget. As rewards are redeemed, the platform's internal billing uses that.
  - Or platform bills monthly. In any case, from user perspective, they set budgets and track usage; from provider perspective, there is an internal account. The SRS can mention that the platform will integrate with a billing system to track actual costs and charges to the client (non-functional maybe).
  - But since they specifically said budget management, likely focusing on usage tracking, not on actual payment to us. So we'll not detail billing beyond perhaps an internal integration mention.
- **FR 3.5.13 Budget Use Policies:** Some organizations have “use it or lose it” budgets each quarter, others roll over unused budget. The system should allow configuration:
  - If a budget period ends, decide whether remaining funds expire or carry to next period or to a general pool.
  - E.g., if Q1 budget $1000, spent $800, do the $200 vanish or get added to Q2? Could be toggled.
  - If not too hard, at least allow manual carryover (admin adjusting Q2 budget accordingly). Automatic carry might be not needed initially.
- **FR 3.5.14 Audit Trail for Budget Changes:** Any creation, update, or deletion of budget, or any override of budget rules (like approval of overspend) shall be recorded in the audit log (who, when, what changed). This is important as budgets are sensitive and for compliance (especially for SOC2, showing controls).

In summary, the Budget Management feature is about **control and visibility**: control by setting limits and possibly gating actions, and visibility by showing how the money is being used in real-time.

**Example Use Case for Budget:**  
Acme Corp sets an annual rewards budget of $50,000. Within that, the HR team has $20k for employee rewards, and the Marketing team has $30k for customer promotions. Jane (HR) tries to send out holiday gifts of $100 each to 250 employees = $25,000, which exceeds her HR budget of $20k. The system will block or require approval because that’s $5k over. She requests an increase; the CFO raises HR’s budget to $25k or transfers some from Marketing if they have excess. Once budget is adjusted, she retries and it's allowed. As employees redeem, the system shows HR budget now has e.g. $24,700 spent (if some not redeemed yet, maybe still $25k allocated with $300 possibly not used if a few didn’t claim). She can see how much each department used at year end. If some portion (like $1k) never redeemed by the expiration of those gifts, maybe next year they might reduce the spent count or CFO notes it as savings.

By meeting these requirements, IncentiveHub ensures companies can trust the platform not to overspend and can easily account for their incentive program expenditures.

### 3.6 User Management and Role-Based Access Control (RBAC)

**Description:** User Management and RBAC features govern how different users access and interact with the platform. In a SaaS platform used by organizations, it's essential to have a robust system for creating user accounts, assigning roles with specific permissions, and managing these accounts (passwords, SSO, activation/deactivation, etc.). Role-Based Access Control means each role (like Admin, Manager, Viewer as defined earlier in Section 2.3) has a set of allowed actions, and the system will enforce those permissions for every operation.

This section describes how user accounts are handled, how roles and permissions are structured, and what administrative functions exist for managing users.

**Functional Requirements:**

- **FR 3.6.1 User Account Creation:** The system shall allow Org Admins (and the platform’s own ops) to **create new user accounts** for their organization. Mechanisms include:
  - An Admin can invite a user by entering their email and selecting a role for them. The system then sends an invitation email to that user with a link to set up their account (set password or use SSO).
  - Alternatively, an Admin can create an account directly with a temporary password to convey to the user (less secure, invitation method preferred).
  - The system should verify that the email is unique within that organization (and probably unique globally or at least unique combination of email+tenant).
  - If using SSO integration (see below), account provisioning might be via SSO (just-in-time creation when they first log in).
- **FR 3.6.2 Roles and Permissions Definition:** The platform shall have predefined roles (as per Section 2.3) with associated permissions:

  - **Administrator:** Can do everything in their org: manage users, configure settings, create budgets, send rewards, view all data, run reports, etc.
  - **Program/Rewards Manager:** Can create/send rewards and campaigns, view and edit those they created (or within their scope), view reports related to their programs, but might not manage other users or global settings.
  - **Finance Manager:** Can manage budgets and view all spending data and reports, possibly can approve requests, but might not send rewards (or maybe they can, up to organization).
  - **Viewer/Read-Only:** Can view dashboards, reports, and perhaps see campaigns (maybe all or those shared with them) but cannot trigger sends or change anything.
  - **(Other roles)**: Possibly if needed, an "Approver" role who only approves pending reward sends or budget changes.

  The system shall have a configuration (likely not UI-exposed in v1 except via fixed roles) mapping roles to permissions. For example, an internal representation like:

  - Admin: permission flags [Manage_Users, Manage_Catalog(for custom items), Manage_Budgets, Send_Rewards, View_Reports, Configure_Integrations, etc.]
  - Manager: [Send_Rewards, View_Reports (own), maybe Manage_Customers list? etc.]
  - Finance: [Manage_Budgets, View_Reports (financial), not Send_Rewards (maybe optional), etc.]
  - Viewer: [View_Reports (all or subset), nothing else].

  Ideally, this is flexible for future where custom roles or adjusting permissions might be needed (some companies might want a custom mix). But initially, fixed roles is fine as long as they cover typical needs.

- **FR 3.6.3 Access Control Enforcement:** For every action in the system, the backend shall enforce that the user has the permission to perform that action:
  - If a user without admin rights tries to access the User Management page, they should be denied (UI should hide it anyway).
  - If a Manager tries to view a reward that belongs to another manager’s campaign (assuming we partition data by owner), either deny or only show if policy allows (some orgs might have managers only see their own data, others might allow all managers to see everything – perhaps configurable).
  - The system must clearly define data visibility rules: by default, Admin sees all data in org; Managers see the data of the campaigns/rewards they created or that are assigned to them; Finance sees all financial data (likely all transactions, or maybe just summary).
  - Example: A manager shouldn't be able to edit another manager’s campaign or cancel their rewards, unless given permission. Possibly there's a concept of team ownership, but we can keep it simple initially: a non-admin user sees what they did and not others, unless there's a share.
  - Implementation wise, this means including organization ID in all queries to isolate data to that org (so user from one company never sees another’s data – crucial multi-tenant isolation).
- **FR 3.6.4 User Authentication:** The platform shall support secure authentication for users:
  - By default, email/password login with strong password requirements (min length, complexity, etc.).
  - Passwords shall be stored hashed (non-functional security).
  - Also support **Single Sign-On (SSO)** for enterprise: specifically SAML 2.0 or OAuth2/OIDC integration. Many enterprises prefer to integrate with their identity provider (like Okta, Azure AD, Google Workspace) so that users use their corporate credentials. The system shall allow an Org Admin to configure SSO for their domain. Possibly an admin can mark that their org uses SSO exclusively (then local passwords maybe disabled for those users).
  - If SSO is configured, user management might happen via SSO (like auto-provision new user on first login, as mentioned).
  - Possibly support Multi-Factor Authentication (MFA) especially for admin accounts if not using SSO (maybe as an option, e.g., TOTP or SMS 2FA).
- **FR 3.6.5 User Profile Management:** Each user should have a profile they can manage:
  - The system shall allow a logged-in user to view and edit their profile info (name, contact info, maybe change password if local).
  - If using local login, allow them to reset password (via forgot password flow sending email).
  - Set their notification preferences (e.g., opt in/out of certain system emails like “reward redeemed notifications” as mentioned).
  - Possibly select language preference (for UI localization).
- **FR 3.6.6 Activate/Deactivate Users:** Admins shall be able to **deactivate or remove a user’s access**:
  - If someone leaves the company or changes role, the admin can disable their account. A deactivated user cannot log in or do anything, but their historical actions and data remain for records (maybe mark them as inactive in user list).
  - Option to delete user entirely might not be given to org admin if needed for audit (maybe platform support can purge if required by GDPR request).
  - Deactivation should be reversible (admin can re-enable if needed).
- **FR 3.6.7 Role Changes:** Admins can change a user’s role (promote someone to admin or downgrade rights). The system should enforce certain constraints (maybe cannot remove own admin rights accidentally leaving no admin).
  - Ideally, at least one admin remains active at all times for an org. If last admin tries to demote themselves, should be blocked or require transferring admin to someone else first.
- **FR 3.6.8 Organization and Tenant Management:** (From the client admin perspective, this might not be directly visible, but as a platform we must maintain an organization entity linking users, data, budgets, etc.)
  - All data entities like rewards, budgets, etc., will have an Org ID to tie to the correct tenant.
  - Org Admin should see an org profile (e.g., organization name, address, maybe logo upload for branding, default settings like time zone, base currency, etc.).
  - Possibly a section where they configure global settings like email templates (putting company logo, choosing email sender address if domain is verified).
  - Also where SSO config resides, webhooks endpoints if they want to add, etc. But those could be in integration section.
- **FR 3.6.9 Audit Logging for User Management:** All user management actions (creating user, deleting, role change, SSO config changes) shall be recorded in audit logs (with who performed it and when), since user accounts are sensitive. This ties with Section 3.7 (Audit Logging).

- **FR 3.6.10 Session Management and Security:** (This is partly non-functional but includes:
  - Possibly allow Admin to force log-out of a user or end sessions (especially if a user is terminated and they were logged in, admin might want to ensure they get logged out).
  - Session timeout: after a period of inactivity (e.g., 30 minutes or configurable), user gets logged out for security, unless “remember me” specifically allowed.
  - Concurrency: If needed, limit how many sessions or devices can be logged in for one user, or at least track it.
  - But these are internal security details. At least mention idle timeout enforcement to align with security best practice.
- **FR 3.6.11 Scalability of Users:** We assume each client org might have a modest number of internal users (maybe dozens at most, since these are admin-type accounts). But in some cases, if say a program manager wants to give read access to many stakeholders, we could have a larger number of viewer accounts. The system should handle that but it's not large like millions, so no big constraints.

**User Roles & Permissions Table:** Below is a table summarizing example roles and what they can do (for clarity and to ensure we have covered differences):

| **Role**                              | **Description**                                                                                                  | **Key Permissions**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Org Administrator**                 | Top-level admin for the organization. Typically responsible for initial setup and ongoing configuration.         | - Manage all users (invite, remove, assign roles) <br> - Configure SSO, integrations, company settings <br> - Create and manage budgets <br> - Full access to reward catalog (including adding custom rewards) <br> - Can send rewards and manage any campaign <br> - View all reports and data across the organization <br> - Manage audit logs and receive all notifications                                                                                                                                                     |
| **Program Manager** (Rewards Manager) | Main user for running reward campaigns or programs. Focused on sending rewards and managing their initiatives.   | - Create and send rewards (single or bulk) to recipients <br> - Create campaigns or groupings for their rewards <br> - Choose from available catalog (cannot modify catalog except possibly marking favorites) <br> - View status of rewards they sent, track redemptions <br> - View reports for their own campaigns (e.g., redemption rates, spend vs budget allocated to them) <br> - Typically cannot manage other users or global settings <br> - May request budget increase or approval (if over budget, triggers workflow) |
| **Finance Manager**                   | User focusing on financial control and analysis of rewards spending. Might be part of Finance or Ops.            | - Create/manage budgets (if delegated by Admin) or at least view budgets <br> - Approve or deny over-budget requests (if approval workflow exists) <br> - View all reward transactions and financial reports (spend by department, etc.) <br> - Likely does not send rewards (or maybe can, but usually not their role) <br> - Cannot manage users (unless also an Admin) <br> - Can export financial data for reconciliation                                                                                                      |
| **Viewer/Read-Only**                  | A user who needs visibility but not action (e.g., an executive sponsor or auditor).                              | - View dashboards and summary reports (perhaps the entire org’s, or could be limited to certain scopes as configured by Admin) <br> - View reward statuses (maybe all, or those relevant) <br> - Cannot send rewards or alter anything <br> - Cannot access configuration or user management <br> - Essentially “look but don’t touch” rights.                                                                                                                                                                                     |
| **Support/Approver** (Optional Role)  | (If implemented) A user who handles support or approvals rather than managing campaigns. Possibly a subset role. | - **Support**: Can view all reward details to help troubleshoot recipient issues (e.g., check if an email was sent, resend a reward if needed) but might not create new ones. <br> - **Approver**: Receives notifications when an approval is required (e.g., budget or high-value reward) and can approve/deny, but not initiate sends on their own. <br> - These could be separate roles or just tasks for Admin/Finance roles.                                                                                                  |

_Table 3.6.1 - User Roles and Permissions:_ The exact permissions can be refined, but this shows how responsibilities are separated. The platform might allow combining roles (e.g., someone can be both Finance and Program Manager if needed). Admin has inherently all permissions of other roles plus more.

- **FR 3.6.12 Multi-Tenancy Isolation:** It’s implicit but worth stating: The system shall strictly isolate data by tenant (organization). No user from one organization can access or see data of another organization. Even if their emails look similar or they guess an ID, the API/queries must always filter by their org context. This is achieved by associating every user with exactly one organization (except platform super-admins) and scoping every request. For example, even URLs or IDs should not be guessable across orgs. This is a crucial security requirement (non-functional as well).

- **FR 3.6.13 Platform Admin (Superuser):** There will be platform-level admin accounts (not belonging to a client org) for the company operating the platform. These accounts can manage any organization (for support, configuration, etc.) Possibly they have a separate interface or using internal tools. This is mostly an internal requirement, but should be noted: those superusers can# Software Requirements Specification for IncentiveHub Rewards Platform

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) document describes the requirements for **IncentiveHub**, a SaaS-based Rewards and Incentives management platform targeted at product managers and business teams. The purpose of this document is to detail all functional and non-functional requirements for the IncentiveHub platform, including its features, behavior, and constraints. It is intended to serve as a comprehensive guide for stakeholders (product managers, developers, designers, and compliance teams) to understand the system's expected capabilities and design criteria. This SRS will ensure that the final product meets business needs for rewarding customers, employees, and partners through a robust, secure, and user-friendly application.

### 1.2 Scope

The IncentiveHub platform will enable businesses to **digitally source, deliver, and track rewards** (e.g. gift cards, vouchers, tangible gifts) to various recipients such as customers, employees, and partners. It will support a wide range of rewards delivery use cases, including: corporate employee gifting, B2B partner incentives, B2C customer loyalty rewards, and research participation incentives. Key functionalities covered in scope include:

- A **Rewards Catalog** of available digital and physical reward options.
- **Reward distribution** features to send rewards individually or in bulk, with tracking from delivery to redemption.
- **Redemption workflows** for recipients to claim or redeem rewards, and corresponding status tracking.
- **Budget management** tools to define and monitor reward program spending limits.
- **Reporting and analytics** modules to measure reward usage and outcomes.
- **User management and role-based access control (RBAC)** to manage different user roles (e.g., admins, managers, finance) and ensure appropriate access.
- **Audit logging** of key actions for accountability and compliance.
- **Integration capabilities** including public APIs, webhooks, and integration with third-party services (e.g. SSO providers, email/SMS gateways, reward vendors).
- **Compliance and security** features to meet data privacy regulations (GDPR, CCPA) and industry security standards (SOC 2, etc.).
- **UI/UX requirements** for an intuitive web interface and positive user experience, including localization support for multiple languages and regions.

Out of scope for this version are features like internal point-based loyalty currency systems, advanced AI-based reward recommendation engines, or built-in tax reporting for rewards (organizations must handle any tax implications of rewards outside the system). This document focuses on the core requirements to support digital reward delivery and tracking in a multi-tenant SaaS environment.

### 1.3 Product Overview

IncentiveHub is a cloud-based application that provides organizations a centralized platform to manage their rewards and incentives programs. It is primarily intended for **product managers** and other business users who need to incentivize various audiences (employees, partners, customers) without building custom reward solutions from scratch. The platform simplifies the process of procuring rewards (like e-gift cards or vouchers), delivering them to recipients around the world, and tracking engagement (redemptions) — all while managing budgets and ensuring compliance.

IncentiveHub will be offered as a multi-tenant SaaS, meaning multiple business clients (tenants) will use the platform securely in isolation from each other, accessing it via web browsers and integrating via APIs. The product aims to streamline diverse incentive use cases on one platform, increasing efficiency and providing visibility into reward program performance. Key benefits include reducing manual effort in sending rewards, preventing reward fraud or misuse through tracking, and improving recipient satisfaction by offering a variety of reward choices delivered promptly.

### 1.4 Definitions, Acronyms, and Abbreviations

- **SaaS** – Software as a Service. A software distribution model in which a third-party provider hosts applications and makes them available to customers over the Internet.
- **Reward** – A gift or incentive (monetary or non-monetary) given to a recipient (customer, employee, partner, etc.) as part of an incentive program. In this document, rewards typically refer to gift cards, vouchers, promo codes, or physical gifts.
- **Recipient** – The end person who receives a reward (e.g., an employee receiving a gift card, a customer receiving a voucher). Recipients are usually not direct users of the platform but interact via reward redemption links or communications.
- **Catalog** – The collection of reward items available in the platform that users can choose from to send to recipients. This includes digital rewards (e.g., e-gift cards) and tangible items (physical gifts) sourced through integrated providers.
- **Redemption** – The act of a recipient claiming or using a reward (e.g., using a gift card code, claiming a voucher). A reward is considered “redeemed” once the recipient has successfully claimed or used it.
- **Product Manager** – In our context, the primary user persona for this platform: a business user who plans and executes incentive programs (for customers, employees, etc.) to achieve business goals (such as boosting engagement, sales, or survey participation).
- **Administrator (Admin)** – A user role on the platform with elevated permissions, typically responsible for setting up the organization’s account, managing users, configuring integrations, and overseeing all reward programs and budgets.
- **RBAC** – Role-Based Access Control. A method of regulating access to the system’s functions and data based on users’ roles within an organization.
- **GDPR** – General Data Protection Regulation. EU regulation governing data privacy and protection for individuals within the EU. Relevant to how personal data (e.g., recipient information) is handled.
- **CCPA** – California Consumer Privacy Act. A data privacy law in California, USA, similar in intent to GDPR, giving consumers rights over their personal data.
- **SOC 2** – Service Organization Control 2. A compliance standard for service providers, focusing on controls around security, availability, processing integrity, confidentiality, and privacy of customer data.
- **API** – Application Programming Interface. In this context, a set of endpoints exposed by the IncentiveHub platform that allow external systems to interact with it (e.g., to trigger sending a reward programmatically).
- **KPI** – Key Performance Indicator. A metric used to evaluate success; for example, redemption rate of rewards, or total rewards sent in a quarter, could be KPIs for an incentive program.
- **Tenant** – A client organization using the multi-tenant platform. Tenant data is isolated from other tenants.
- **Use Case** – A scenario describing how users interact with the system to achieve a goal. Used to validate that requirements support real-world operations.

_(Note: A Glossary in Section 8 provides additional definitions of terms used in this SRS.)_

### 1.5 References

The following references or standards are relevant to the requirements in this document:

- **GDPR (EU Regulation 2016/679)** – Regulation on data protection and privacy in the European Union, which the platform must comply with when handling personal data of EU residents.
- **CCPA (California Consumer Privacy Act of 2018)** – California state law on consumer data privacy, applicable for handling data of California residents.
- **SOC 2 Trust Services Criteria** – Industry standard criteria for managing customer data in the context of security, availability, confidentiality, processing integrity, and privacy. The platform will be developed to meet SOC 2 Type II requirements for security and confidentiality.
- **ISO/IEC 27001** – International standard for information security management. (The platform’s security controls and processes will align with ISO 27001 best practices, though formal certification is a future consideration.)
- **OWASP Top 10** – Open Web Application Security Project Top 10 security risks. The development will consider OWASP Top 10 to ensure mitigation of common web application vulnerabilities (like XSS, SQL injection, etc.).
- **WCAG 2.1 (AA)** – Web Content Accessibility Guidelines version 2.1, level AA. Guidelines for accessible web interface design which will inform UI requirements to support users with disabilities.

### 1.6 Overview of Document

The rest of this SRS document is organized as follows:

- **Section 2 Overall Description:** Provides a high-level overview of the product including its context, user characteristics, assumptions, and dependencies.
- **Section 3 System Features and Functional Requirements:** Detailed description of the platform’s features grouped by functional areas (Catalog Management, Reward Distribution, Tracking, Redemption, Budgeting, User Management, etc.), with specific requirements enumerated for each.
- **Section 4 UI/UX Requirements:** Outlines the user interface and user experience expectations, including key UI features, usability guidelines, and design considerations for the platform.
- **Section 5 Non-Functional Requirements:** Describes requirements related to performance, security, compliance, availability, scalability, maintainability, and other quality attributes the system must fulfill.
- **Section 6 System Architecture Overview:** Presents a conceptual overview of the system’s architecture, including major components, how they interact, and how third-party integrations are incorporated.
- **Section 7 Use Case Scenarios & User Journeys:** Illustrative scenarios and step-by-step user journeys for typical use cases (employee gifting, partner incentives, customer rewards, research incentives), demonstrating how the platform will be used in practice.
- **Section 8 Appendices:** Additional supporting information such as detailed tables for roles and permissions, reward type examples, and a glossary of terms. (Any detailed data or lists that support the requirements are included here for reference.)

Each requirement in this document is uniquely identified and described. Functional requirements are generally labeled “FR” (for example, FR-1, FR-2) and non-functional requirements as “NFR” where needed, though for readability they may be presented in bullet or tabular form rather than a single exhaustive list. This document is intended to be updated as the project evolves, with version control to track changes in requirements.

## 2. Overall Description

### 2.1 Product Perspective

IncentiveHub is a **new, standalone SaaS application** developed to streamline rewards and incentives management. It is not a component of an existing product but will integrate with various external systems (e.g., email/SMS services, SSO identity providers, and reward suppliers) as needed. The platform adopts a **multi-tier architecture** and a **multi-tenant model**, meaning a single instance of the application serves multiple client organizations, with data partitioning to ensure each organization’s data is isolated and secure.

From a **product perspective**, IncentiveHub acts as a central hub that connects those who **issue rewards** (the business users/administrators) with those who **receive rewards** (employees, customers, partners), along with the vendors who **fulfill rewards** (gift card providers, etc.). It sits between the business and the reward fulfillment channels:

- Upstream, it interfaces with **business systems and users** (e.g., a product manager using a web UI or an external application calling the API to trigger a reward).
- Internally, it manages business logic like selecting rewards from the catalog, logging transactions, enforcing budgets, etc.
- Downstream, it connects to **delivery mechanisms** (such as email or other messaging services to send reward links/codes) and to **reward providers** (e.g., third-party gift card services or vendors that supply the actual reward items).

The platform’s design will be modular, consisting of components for catalog management, reward processing, user management, etc. It will leverage cloud infrastructure for scalability and reliability. Figure 6.1 in the System Architecture section provides a high-level visual overview of how these components interact within the environment.

### 2.2 Product Functions

At a high level, the key functions of the IncentiveHub platform include:

- **Reward Catalog Management:** Provide a comprehensive catalog of reward options (e.g., gift cards to various retailers, prepaid vouchers, merchandise) which users can browse and choose from. This includes maintaining item details (description, value, category, availability region, etc.) and updating availability or adding new reward types as needed.

- **Reward Issuance (Delivery & Distribution):** Enable users to send rewards to recipients easily. This covers single reward sending (ad hoc rewards) and bulk distribution (mass incentives), scheduling deliveries, personalizing messages, and choosing delivery methods (email, SMS, etc.). The system handles interacting with external providers to actually fulfill the reward (e.g., calling an API to generate a gift card code) and deliver it to the recipient.

- **Reward Tracking & Lifecycle Management:** Track each reward from the moment it’s initiated to the point it’s redeemed (or expires). The system logs statuses like sent, delivered, opened, redeemed, or failed. Users can monitor reward delivery in real-time, see which rewards are unclaimed, send reminders, or cancel/reissue rewards if needed.

- **Reward Redemption Support:** Provide a smooth experience for recipients to redeem their rewards. This includes hosted redemption pages or links where recipients can view their reward (e.g., reveal a gift card code or enter shipping information for a physical gift), choose from multiple reward options if offered, and confirmation of redemption. The system ensures that each reward can only be redeemed once and handles any errors (e.g., an expired link or an already-used code) gracefully.

- **Budget Management:** Allow organizations to allocate and manage budgets for their rewards programs. Users (especially finance or admins) can set spending limits (overall or for specific campaigns/teams), track the amount spent vs. remaining budget, enforce limits (prevent or require approval for actions exceeding budget), and adjust budgets as needed. The platform may support multiple budget categories or periods (e.g., quarterly budgets, campaign-specific budgets).

- **User Management and RBAC:** Provide administrative functions to manage user accounts within each organization using the platform. This includes creating users, defining roles/permissions (e.g., admin, program manager, viewer), and controlling access to features and data based on role. For example, one user may have rights to send rewards and manage campaigns, while another can only view reports. Additionally, the system will integrate with single sign-on solutions to streamline authentication where needed.

- **Audit Logging:** Record a detailed audit trail of important actions in the system for security and compliance. This includes logging user activities such as login attempts, reward distributions, changes to budgets, modifications of user roles, and configuration changes. Audit logs are accessible to authorized users (e.g., admins) to review who did what and when, supporting accountability and external compliance audits (like SOC 2).

- **Reporting and Analytics:** Offer reporting tools and dashboards for users to analyze the performance of their reward and incentive programs. Key metrics include number of rewards sent, redemption rates, total spend, budget utilization, and program ROI indicators. Users should be able to generate summary reports (with charts) and detailed logs (with data export) to evaluate effectiveness and present results to stakeholders.

- **APIs and Integrations:** Provide external interfaces to integrate the IncentiveHub platform with other systems. This includes a robust RESTful API for triggering rewards and retrieving status programmatically (useful for integration into customer applications or workflows), as well as webhooks or callbacks to notify external systems of events (like a reward redeemed). Integration capabilities also cover connecting with third-party services such as email/SMS gateways (for delivery), SSO identity providers (for user login), HR or CRM systems (for importing recipients), and reward vendors (for sourcing the rewards).

- **Compliance and Security Features:** Ensure the platform operates within required legal and security frameworks. This includes protecting personal data (encryption, access control), obtaining necessary consents or providing opt-outs for communications if needed, allowing data deletion or export per GDPR/CCPA rights, and maintaining high security standards (secure coding, penetration testing, etc.). Role-based access and audit logs (as mentioned) contribute to this, as do features like configurable data retention policies.

- **Localization and Multi-Currency Support:** Support multiple languages and regional settings in the UI and in reward offerings. For example, a user should be able to view the interface in English, Spanish, French, etc., and send rewards that are appropriate for the recipient’s country (both in terms of language of the message and type of reward/currency). Date/time formats, currency conversion for budgets, and other localization aspects will be handled to make the platform usable globally.

These functions will work together to provide a seamless end-to-end solution for incentive management. In practice, a product manager could log into IncentiveHub, create a campaign (with a defined budget), select a set of rewards from the catalog, send those rewards to a list of recipient emails (either manually or via an integration trigger), and then use the platform to monitor who redeemed their rewards and how much budget remains, all within one system.

### 2.3 User Classes and Characteristics

The platform will be used by several distinct user classes, each with different needs and permissions. Below are the primary user roles (within a client organization) and their characteristics:

- **Organization Administrator (Org Admin):** This user class represents the primary administrator(s) of the platform for a given client organization. Typically an IT lead or a program owner, the Org Admin has the highest level of permissions within their organization’s tenant. They can manage all aspects of the account: user accounts and roles, global settings, budgets, integrations, and have full visibility into all reward campaigns and data. They ensure the platform is configured properly (e.g., SSO integration, adding company branding elements, setting default settings). They are also responsible for creating other user accounts (managers, viewers, etc.) and assigning appropriate roles. Characteristics: tech-savvy, security-conscious, needs full control; likely relatively few people (one or two per organization).

- **Program/Rewards Manager:** This is the primary user type for which the platform is targeted (often the _product manager_, marketing manager, HR manager, or whoever runs the incentive programs). Rewards Managers are the users who create and manage reward campaigns. They select rewards from the catalog, define recipient lists or criteria, send out rewards, and monitor their campaigns’ progress. They have access to create and edit campaigns, view results for their campaigns, and generally manage day-to-day operations of reward distribution. Depending on organizational setup, a Rewards Manager might only see campaigns they created or those for their department, or they might have access to all campaigns (if not limited by role scope). Characteristics: business-oriented, goal-focused (wants to increase engagement, sales, etc.), expects an easy-to-use UI to quickly send rewards and check status; not necessarily deeply technical.

- **Finance/Budget Manager:** In some organizations, financial controllers or budget owners may use the platform to oversee spending. This user class focuses on the **budget management** and **reporting** aspects. They set up budgets or cost centers for reward programs, approve or monitor expenditures, and run spend reports. They might not initiate reward sends themselves but need visibility into how funds are used. They typically have permissions to adjust budgets, view all transactions, but perhaps not to create campaigns (depending on internal policy). Characteristics: detail-oriented, concerned with cost control and ROI, may use export reports for accounting reconciliation.

- **Viewer/Read-Only User:** This class includes any stakeholders who need to see information on the platform but not make changes. For instance, an executive or a client of the business might be given read-only access to dashboards to observe program performance. Or a compliance officer might be given access to audit logs. These users can log in and navigate through reports, campaign statuses, etc., but cannot trigger any actions (no sending rewards, no editing). Characteristics: could be high-level (needs summary information) or support role (needs to verify data), will use primarily the reporting UI or read-only views.

- **Recipient (External User):** Technically not a user of the platform in the sense of logging into the main application, but they are a crucial actor. Recipients are employees, customers, partners, or research participants who receive the rewards. Their interaction is via the **redemption process** – for example, clicking an email link to claim a gift card. They expect a simple, quick way to get their reward without needing an account or complicated steps. The platform must cater to recipients by providing a user-friendly redemption page (web interface, likely mobile-friendly) and possibly choices of reward. We consider their needs in the design of the redemption workflow (clear instructions, support if issues, etc.). Recipients vary widely in background (could be tech-savvy or not, internal or external to the company), so that part of the system must be extremely simple and reliable.

- **System Administrator (Platform Operator):** (This is an internal role, not within a client organization, but worth mentioning for context.) The team running the IncentiveHub service (the vendor or IT ops) will have superuser access to manage the overall system, configure the reward catalog, and oversee multi-tenant operations. They are responsible for uploading new rewards to the global catalog, maintaining integrations with suppliers, and handling any global configuration (like turning features on/off, doing system maintenance). This SRS primarily addresses requirements for client-facing functionality, so this role’s needs (like internal admin tools to manage the entire platform or content) are mentioned where relevant but not a focus of this document’s scope.

**Roles and Permissions:** The platform will implement role-based access control to manage what each user class can do. A summary of roles and their permissions is illustrated in **Table 3.6.1** in section 3.6. In general, Org Admins have full permissions within their org; Program Managers have permissions to manage rewards/campaigns and view related data; Finance Managers have permissions around budgets and financial data; Viewers have view-only access to designated sections. These roles might be configurable per organization (for example, an organization might decide to merge program and finance roles for a single user, or require dual approval for some actions – such specifics can be configured on top of the base roles).

### 2.4 Operating Environment

The IncentiveHub application will operate in a **cloud-based environment** accessible primarily via web browsers. Key aspects of the operating environment include:

- **Client Side:** Users will access the platform through a secure web application. The web app will be compatible with modern web browsers (at minimum, the latest versions of Google Chrome, Mozilla Firefox, Microsoft Edge, and Safari) on desktop operating systems (Windows, macOS, Linux). The UI will be responsive to support use on various screen sizes, including tablets and smartphones, although primary usage is expected on desktop for administrative tasks. No software installation is required on client machines; only an up-to-date browser and internet connection. The interface will use standard web technologies (HTML5, CSS3, JavaScript). For mobile recipients (e.g., an employee opening a reward link on their phone), the redemption pages will be mobile-friendly via responsive design, but there will not be a separate native mobile app in the initial scope.

- **Server Side:** The platform’s server-side components will be hosted on a cloud platform (e.g., AWS or Azure). It will likely consist of application servers (running the web backend and APIs), database servers for persistent storage, and ancillary services (for caching, message queuing, etc.). The environment will have separate instances for development, testing, staging, and production to allow safe development and deployment practices. The production environment will be scalable across multiple servers/instances to handle load and provide redundancy. Operating systems used on servers will be appropriate for the chosen tech stack (likely Linux-based for web servers). The database is expected to be a relational DBMS (such as PostgreSQL or MySQL) for core data, with potential use of NoSQL or in-memory stores for specific needs (like caching catalog data or storing session info).

- **Network and Security:** The application will be accessed via HTTPS over the public internet. It will enforce TLS 1.2+ for all communications to ensure data in transit is encrypted. The service endpoints (web and API) will sit behind a load balancer and possibly a web application firewall (WAF) for security. Integration points to external services (like reward providers or email gateways) will also be over secure APIs. The environment will include monitoring and logging infrastructure to track performance, errors, and security events. The system will be deployed across multiple availability zones or data centers to ensure high availability (detailed in Section 5.4).

- **Constraints from Operating Environment:** Since it’s SaaS, the system must be multi-tenant, meaning careful separation of data by tenant in the database and proper authentication to ensure users only access their organization’s data. The environment will likely use containerization or virtualization for deployment, which implies that the software should be stateless where possible (session state stored in a shared store or sent to client) to allow horizontal scaling. The cloud environment also provides the ability to auto-scale resources based on usage patterns, which the application should be designed to leverage (for example, background processing workers scaling up if many reward emails need sending). All these factors impose design constraints (like using stateless services, externalizing configuration, etc.) which are considered in architecture, but from a requirements perspective, it means the system must **behave correctly in a distributed, dynamic cloud environment** and maintain consistency and performance as it scales.

### 2.5 Design and Implementation Constraints

The development of IncentiveHub must consider several constraints:

- **Regulatory Compliance:** As a major constraint, the system design must ensure compliance with GDPR, CCPA, and other privacy/security laws. This affects how data is stored (e.g., using encryption for personal data), data residency if required (e.g., EU user data may need to reside in EU data centers if clients demand), and features like data deletion or anonymization. It also influences UI (e.g., showing privacy notices or obtaining consent for tracking if needed).

- **Security Standards:** To achieve SOC 2 compliance and overall robust security, certain design constraints are imposed. For example, all user authentication must be designed to allow integration with SSO (SAML/OAuth2) and enforce strong password policies for non-SSO logins; all actions need to be permission-checked (RBAC) which influences how the application logic is structured; audit logging must be built into the system from the start since retrofitting it is hard. The system must also avoid storing sensitive data unnecessarily (for instance, do not store plaintext reward codes if not needed, do not store credit card information at all by using external payment processors).

- **Technology Stack Decisions:** The choice of tech stack might impose constraints. For instance, if the team chooses a certain web framework or database, there might be limitations on maximum data throughput or specific libraries available for features like PDF generation of reports, etc. While this SRS does not dictate implementation tech, it assumes the solution will use proven enterprise technologies that support required features (e.g., a robust scheduling library to schedule future sends, or a reliable job queue for handling bulk email sends). If any third-party components are to be used (like a particular gift card provider’s SDK), compatibility and licensing could be constraints.

- **Multi-tenancy and Scalability:** The system must be designed as multi-tenant from the ground up. This is a constraint meaning every database query or data model must include tenant isolation (like an Org ID). Also, heavy operations (like sending thousands of emails) must be handled asynchronously to not block UI, implying the need for a message queue or background worker system – this is an architectural constraint that influences design (we cannot do everything in a single request/response thread). The constraint ensures that one tenant’s heavy usage doesn’t starve others (so proper resource management, maybe per-tenant rate limiting, might be needed at some level).

- **Integration Constraints:** The platform will integrate with external services (SSO, email, reward providers). We are constrained by those services’ availability and API limits. For example, a gift card provider might have a rate limit on API calls or a certain format for requests/responses we must adhere to. The design must accommodate retries and fallbacks if an external service is down. Also, the system should be flexible to swap out providers – e.g., if we initially integrate Provider A for gift cards but later need Provider B, the integration layer should be abstracted (likely a plugin/adapter pattern for reward providers).

- **UI/UX Constraints:** The UI should follow the company’s design language and be consistent. If there are existing style guides or branding requirements for the platform, they must be followed. Also, accessibility standards (WCAG) impose constraints like color contrast and keyboard navigation requirements. Additionally, since product managers are busy individuals, the UI should be optimized for efficiency – a constraint might be “no process for sending a reward should take more than N clicks” or “the system should respond to any user action within 2 seconds to maintain responsiveness,” which influences design and performance considerations.

- **Time and Release Constraints:** (Project management constraint) If this SRS corresponds to an initial version release, some features might be prioritized or deferred. For example, perhaps full localization might be planned but only English is delivered in version 1 (with the framework in place for others). These kinds of constraints (phased implementation) are typically documented to manage stakeholder expectations, but for this SRS we assume the end vision of the product. If needed, it can be noted that certain features are “Phase 2” or optional, but all listed features here are considered in scope unless explicitly labeled future.

In summary, the constraints highlight that the platform must be built with security, compliance, and scalability in mind from day one, using an architecture conducive to multi-tenant cloud deployment, and a UX that meets enterprise usability standards. All of these constraints have influenced the requirements detailed in Section 3 onward.

### 2.6 Assumptions and Dependencies

To clarify the requirements, the following assumptions and external dependencies are noted:

- **User Base Assumptions:** It is assumed that users of the platform (Admins, Managers, etc.) will have basic internet and web application proficiency. No advanced technical knowledge (like programming) is required for normal operation. For recipients, we assume they have email or phone access to receive digital rewards and internet access to redeem their reward. We also assume recipients trust the sender enough to click the reward link (hence the importance of allowing companies to customize branding on communications to reassure recipients).

- **Reward Fulfillment Partners:** The platform depends on third-party **reward providers** (e.g., gift card aggregators, retailers, or fulfillment companies) to actually fulfill the rewards. We assume that these providers offer reliable APIs or services to procure digital codes or trigger physical shipments, and that they will provide inventory of rewards (e.g., a selection of gift card brands) as agreed. The list of available rewards in the catalog is therefore dependent on partnerships or integrations with these external systems. If a provider changes their API or a certain reward becomes unavailable, timely updates on our side will be needed (this is a dependency risk). We plan to integrate with well-established providers that offer a wide catalog (for example, a gift card API that provides hundreds of brand options globally).

- **Email/SMS Delivery:** We assume the availability of robust email and SMS gateway services for delivering reward notifications. The platform will integrate with an email service (like SendGrid, AWS SES, etc.) and possibly an SMS service (like Twilio) for text message delivery. It is assumed that recipients’ email addresses and phone numbers are valid and that emails/texts will successfully reach them. However, as bounce-backs can happen, the system will handle undeliverable messages (the dependency is that we receive bounce notifications or can query status from the email service, which our system will use to flag those issues).

- **Integration with Client Systems:** We assume that for features like Single Sign-On, the client organization will provide necessary information (e.g., their SAML identity provider details) and that their environment supports standard protocols. Similarly, if the platform is to import data from an HR or CRM system, it’s assumed those systems have an export or API capability that can be used (or at least the client can provide CSV files in a consistent format). While the platform will provide APIs and import tools, the usefulness is dependent on the client’s ability to use them or their IT support to integrate.

- **Budget and Finance:** We assume that companies using the platform will handle funding of rewards externally (e.g., via prepaid deposits or being billed). The platform will track spending against budgets but likely will not handle actual payment processing for each reward in the initial phase. Instead, we assume either a pre-funded model (the company prepays an account from which rewards draw down) or a post-pay model (monthly invoicing for rewards sent). In either case, our system might integrate with a payment/billing system to track cost per client and support invoicing. This is an internal dependency (that our billing system or process is in place). The specific money flow (e.g., charging credit cards) might rely on third-party payment gateways but is largely outside the user-facing scope, except that it intersects with budgets.

- **Legal/Compliance Use by Clients:** We assume that clients will use the platform for legitimate purposes of rewarding and have obtained any necessary consent from recipients to contact them. For instance, if a business is sending a reward to a customer, we assume that the customer has agreed to receive communications (or at least that sending a one-time reward email is within permissible communication under that business relationship). The platform will provide tools to comply (like opt-out management or including an explanation in the email of why the person is receiving a reward), but it assumes the client bears responsibility for the legality of whom they choose to send rewards to.

- **Dependency on Time and Regional Settings:** We assume that the system clock and time zone settings in the environment are properly configured (likely using UTC internally and converting to local time zones in UI) so that scheduling and time-stamping functions work correctly. Also, currency exchange rates (if needed for currency conversion in multi-currency budgets or showing equivalent values) will be fetched from a reliable source – this is a dependency on an external forex rate API if that feature is implemented. (In absence of real-time forex, an admin could set exchange rates manually in settings.)

- **Hardware and Scaling:** We assume that the cloud infrastructure can scale to meet our needs, given proper configuration. The system is expected to handle potentially tens of thousands of rewards being processed (sent or redeemed) per day across all tenants, but should usage exceed expectations, we assume the infrastructure (with possible vertical or horizontal scaling) can be upgraded without requiring fundamental software changes. This is tied to using scalable services (like managed databases that can be upgraded, or auto-scaling groups for application servers).

In summary, the success of the platform is dependent on cooperation between it and external services (for identity, communication, and reward fulfillment) and on clients using it as intended within legal bounds. These assumptions and dependencies will be revisited periodically; if any assumption proves false, requirements might need adjustment (for example, if clients demand integrated payment handling, that would become an additional requirement in a future phase).

## 3. System Features and Functional Requirements

This section details the functional requirements of the IncentiveHub platform, grouped by major feature areas. Each subsection describes a feature or module of the system, followed by specific requirements. The requirements are written in a descriptive manner; key requirements are highlighted with “**The system shall…**” or an **FR-x** label for clarity. Tables and lists are used to summarize certain sets of requirements (e.g., user roles, reward types) where appropriate.

### 3.1 Reward Catalog Management

**Description:** The Reward Catalog is a core component providing an organized list of all reward options that can be delivered through the platform. It includes digital rewards (like e-gift cards, e-vouchers, coupon codes) and physical rewards (like merchandise or gift items) that can be sourced and fulfilled. Product managers (and other users) will browse this catalog when choosing rewards to send. The catalog may be global (managed by the platform provider) but should be filterable and configurable per client (e.g., an organization might disable certain reward types or add custom rewards of their own). This section describes how the catalog is managed and presented.

Key capabilities include viewing reward details, searching and filtering the catalog, selecting rewards (for sending or to include in a campaign), and possibly customizing certain reward entries (like adding a custom reward item that only their organization uses). The catalog data will be populated via integration with external suppliers or manual input by a system admin. For digital rewards, inventory is typically not limited (codes are generated on demand via a provider), but for physical items or limited-stock items, availability needs to be indicated. Pricing information (cost to the company for each reward) also needs to be shown for budgeting purposes.

**Functional Requirements:**

- **FR 3.1.1 Catalog Listing:** The system shall provide a user-friendly **Catalog page** where users can browse all available rewards. Each catalog item shall display key information such as reward name, category (e.g., “Retail Gift Card” or “Travel Voucher” or “Merchandise”), value or denomination (e.g., $50, or specific item description), and type (digital vs physical). If relevant, a thumbnail image or logo for the reward (e.g., the retailer’s logo for a gift card) shall be shown to help users quickly recognize the brand or item.

- **FR 3.1.2 Reward Details:** The system shall allow users to click on or select a reward item to view its **detailed information**. This includes a description of the reward, terms and conditions (if any, e.g., “Card expires in 1 year” or “Valid only in US stores”), available denominations (for gift cards, if multiple values are available), delivery format (e.g., “Code delivered via email” or “Physical shipment”), and **cost information**. The cost information should clarify what sending this reward will deduct from the budget. For example, if a $50 gift card has no additional fees, the cost is $50; if a physical item has shipping or fulfillment fee, it should indicate the total cost. If the platform charges a service fee, that might be factored in (though in many cases, cost = face value for simplicity).

- **FR 3.1.3 Search and Filter:** The system shall provide **search and filtering** functionality on the catalog. Users shall be able to search by reward name or keyword (e.g., “Amazon” to find Amazon gift cards) and filter by categories such as:

  - Reward Type: Digital vs Physical.
  - Category/Industry: e.g., Retail, Dining, Travel, Experiences, Charity (donation vouchers), etc.
  - Value Range: filter rewards by their monetary value or cost (e.g., show only rewards worth $100 or less).
  - Region/Currency: filter to show rewards available in certain regions or currencies (e.g., show only rewards that can be redeemed in Europe, or only rewards priced in USD).
  - Vendor/Brand: if relevant, a filter by brand (all rewards from a specific provider, like “Amazon” or “Starbucks”).

  These filters help narrow down choices, especially as the catalog could contain hundreds of items.

- **FR 3.1.4 Availability by Region:** The system shall handle region-specific availability for rewards. Each reward item in the catalog shall have metadata indicating in which countries or regions it can be delivered or redeemed. For example, a “$50 Amazon.com Gift Card” might be tagged as redeemable only on Amazon’s US site (useful for US recipients), whereas an “Amazon.de Gift Card” is for Germany. When a user is planning to send a reward to recipients in a certain country (which the user might indicate by choosing locale or deducing from recipient list), the system should help by filtering or warning if a selected reward is not suitable for the recipient’s region. _(If the platform doesn’t know recipient region at selection time, at least a note in the reward detail should say “Valid in US only” etc.)_

- **FR 3.1.5 Custom/Client-Provided Rewards:** The system shall allow for **custom rewards** to be added by an organization (if they have something unique to offer). Examples: a company might want to offer “Company Branded Swag Box” that they will fulfill internally, or “Extra Day Off Certificate” as a reward for employees. These are not sourced from the global catalog providers. For such cases, an Org Admin should be able to create a new reward entry visible only to their organization’s users. The entry would have a name, description, perhaps an image, and a way to mark how it’s fulfilled (could be “manual fulfillment” which just records that someone chose it and then the company takes action offline). This is an advanced feature and may be optional in initial release; if implemented, the system will clearly mark custom rewards vs standard ones. Custom rewards still need to be tracked (e.g., if someone selects it, mark it as redeemed or fulfilled manually by admin later). This requirement ensures flexibility for unique incentive ideas beyond the standard catalog.

- **FR 3.1.6 Catalog Update and Synchronization:** The system shall regularly **update the catalog** entries via its integration with external providers. If a provider adds new gift card brands or if an item becomes unavailable, the changes should reflect in the catalog. This might happen via automated sync (e.g., a daily job to fetch current catalog from provider API) or via manual input by a system administrator. From the user perspective, the catalog is always up-to-date. If a user tries to select a reward that just went out-of-stock or is discontinued, the system shall either hide it or inform the user upon selection attempt and prevent sending it. (This ties into error handling in the sending process, but it starts with having current catalog data.)

- **FR 3.1.7 Pricing and Currency Handling:** The catalog should display reward values in a way that’s clear to the user. For monetary rewards (like gift cards), the “value” is typically the same as cost (e.g., a $50 gift card costs $50). For foreign currency gift cards, the system might list them as “£50 British Airways Voucher” and if the user’s budget base currency is different, it may also show an approximate conversion (optional). **The system shall support multi-currency display**: if a user’s organization base currency is USD but they are viewing a reward in EUR, the system could show “€50 (approximately $55)” based on latest exchange rates for informational purposes. (Actual billing may happen in base currency – more in Budget section.) This helps product managers understand cost implications. If real-time conversion is complex, at minimum the system shows the value in the reward’s native currency and a note that currency conversion may apply.

- **FR 3.1.8 Permissions for Catalog Viewing:** Generally, all logged-in users in an org (except perhaps some restricted viewer roles) should be able to view the catalog. The system shall allow configuration such that some roles (like a basic Viewer) might not need to see all details. But likely, the catalog is accessible to Program Managers and Admins who actually send rewards. If needed, an admin could restrict certain categories for their organization. For instance, an admin might toggle off “Alcohol” category gift cards if that doesn’t align with company policy. **The system shall provide Org Admins the ability to configure catalog visibility** by category or item (basically hiding certain reward types from their organization’s view), to enforce their internal policies. This is an optional but useful control for compliance or culture reasons.

- **FR 3.1.9 Catalog Performance:** The system shall be optimized so that browsing the catalog is fast and responsive. Even if there are hundreds of items, users should be able to find items quickly (through search/filter as above). This is more of a performance consideration, but from a functional perspective, the catalog queries should be efficient. If needed, implement paging or infinite scroll to not overload the page. This requirement ensures a smooth browsing experience; see performance NFRs for specifics.

- **FR 3.1.10 Content Management for Catalog:** The text and images in the catalog may need to be updated (e.g., a description change or uploading a new image for an item). This will be done by the platform’s internal team or via the integration. The system shall allow updates to catalog content without requiring a full software release (for instance, through an internal admin interface or by re-sync from provider data). If a reward is temporarily unavailable, the system should mark it as such (e.g., “Out of stock” label) or hide it. Users attempting to select it should be prevented. This ties into reliability of the catalog data.

**Table 3.1 - Examples of Reward Types in Catalog:**  
To illustrate the diversity of the catalog, below is a table of example reward types that IncentiveHub might offer and their characteristics:

| **Reward Type**             | **Description**                                                                                                     | **Delivery Method**                                    | **Example Items**                                                                       |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| **Digital Gift Card**       | Prepaid cards for retailers or services, delivered as codes or electronic vouchers.                                 | Code via Email/SMS (digital)                           | Amazon e-gift card, Starbucks e-card, Uber voucher, App Store code                      |
| **Physical Gift**           | Tangible items or merchandise sent to recipient’s address. Often fulfilled via a partner or e-commerce integration. | Shipped to Address (physical)                          | Company swag box, Branded apparel, Electronics gadget (e.g., headphones)                |
| **Prepaid Visa/Mastercard** | General-purpose prepaid debit cards, loadable with a specified amount, often branded.                               | Physical card mailed, or digital card info via email   | $100 Prepaid Visa Card (physical or virtual), MasterCard eReward (virtual code)         |
| **Experience Voucher**      | Tickets or vouchers for experiences (travel, events, etc.).                                                         | Email with booking code or instructions                | Airline ticket voucher, Hotel gift certificate, Concert tickets code                    |
| **Donation/Charity Gift**   | A charitable donation made on behalf of the recipient to a chosen charity.                                          | Email confirmation (digital)                           | $50 Donation to Red Cross (recipient gets a note or certificate)                        |
| **Coupon/Promo Code**       | A code granting a discount or free service (often for the company’s own product).                                   | Code via Email (digital)                               | 20% off next purchase code, Free month subscription code                                |
| **Custom Reward**           | Company-specific incentive defined by the user organization. Fulfillment might be manual or outside platform.       | Varies (could be email certificate or manual delivery) | “One Extra Vacation Day” certificate, “Lunch with CEO” experience, “Custom Gift Basket” |

_Table 3.1:_ The platform’s catalog can include a wide range of reward types. Each type has different fulfillment methods and use cases. The system architecture (especially integration) must handle each appropriately (e.g., interfacing with gift card APIs for digital cards, or prompting for address for physical gifts). The catalog will categorize these so users can easily choose suitable rewards for their audience.

### 3.2 Reward Delivery and Distribution

**Description:** This feature covers the process of sending rewards to recipients. Product managers or other authorized users will initiate reward delivery through the platform. This can happen in various ways: individually sending a reward to a single recipient (ad hoc gifting), sending in bulk to a list of recipients (mass distribution for a campaign), or automatically via triggers through the API (for example, a customer completes a certain action and the system sends a reward without manual intervention). The platform must handle all these cases in a user-friendly and reliable manner.

When sending a reward, the user typically will: choose the reward from the catalog, specify details (such as value if applicable, quantity if multiple recipients, and any message), specify the recipient(s) (enter emails or select a pre-uploaded list), and then confirm sending. The system then orchestrates the fulfillment: contacting the reward provider to generate the gift (if needed) and delivering the notification (usually via email) to the recipient with instructions or a link to redeem. This sub-system also deals with scheduling (send now or at a future date), personalization of messages, and ensuring that the sending action is logged and reflected in budgets.

**Functional Requirements:**

- **FR 3.2.1 Single Reward Sending:** The system shall allow a user to send a reward to a single recipient in a straightforward workflow. For example, a Product Manager can choose “Send Reward” from the dashboard or menu, then: select a reward from the catalog (e.g., $50 Gift Card), enter the recipient’s details (at minimum, an email address; possibly name and a personal note), and confirm. The system shall then process this request by reserving or generating the reward (through the provider API) and sending an email to the recipient with the reward details or a link to redeem (depending on how that reward is delivered). This process should ideally be done in a few simple steps (usability focus). After sending, the user should see a confirmation that the reward was sent successfully (or an error message if something went wrong).

- **FR 3.2.2 Bulk Rewards Sending (Batch Distribution):** The system shall support sending a reward (or rewards) to multiple recipients in one operation. Users (with permission) can initiate a **bulk send** by either selecting multiple recipients or uploading a list. Requirements for bulk sending:
  - The user can specify a list of recipients. This can be done by uploading a CSV file containing recipient data (e.g., email, name, maybe other fields like employee ID or any personalization fields), or by selecting a pre-defined group (if the system supports storing groups of contacts), or manually entering multiple emails separated by commas/newlines.
  - The user selects the reward (or possibly multiple different rewards if each recipient gets a different one, though usually bulk means the same reward to all; if per-person customization is needed, that could be done via CSV specifying which reward each gets if the system supports it).
  - The user can compose a single message template that will be sent to all, with placeholders for personalization (like inserting each recipient’s first name). **The system shall support message templates** with basic placeholders (e.g., `{{Name}}`) that get replaced per recipient.
  - The system shall validate the list before final submission: e.g., check that email addresses are in a valid format, flag duplicates, and perhaps cross-check against any do-not-contact list (if someone previously opted out, though that might be handled at send time too).
  - Upon confirmation, the system will initiate sending to all those recipients. For potentially large lists, this should be handled asynchronously (placed in a queue for background processing) so the user doesn’t have to wait for every email to send. The user should be informed that the send is in progress and possibly given a way to monitor progress (like “200 of 500 emails sent” status, or at least a notification when done).
  - **FR 3.2.2a:** The system shall create individual reward entries for each recipient in the bulk list, so they can be tracked separately (e.g., each with its own status).
  - **FR 3.2.2b:** If any sends in the bulk fail (e.g., invalid email causing bounce or provider error), the system shall record those failures and make it easy for the user to see which recipients did not get their reward and why, so they can take corrective action (like fix an email and resend to just those).
- **FR 3.2.3 Scheduling Rewards:** The system shall offer an option to **schedule a reward send for a future date/time**. For example, an HR manager may want to schedule birthday e-cards ahead of time or a product manager might schedule sending all rewards on a specific campaign launch date. When scheduling:
  - The user will pick the date and time for the send (the UI should allow date/time selection, possibly with timezone if needed).
  - The system must store this and ensure the rewards are sent at approximately that date/time.
  - The system should account for time zones properly; likely storing in UTC internally and converting to the user's timezone in the UI.
  - The system should list scheduled outgoing rewards in a “Scheduled” view so the user can verify or cancel them before they execute.
  - **The system shall ensure that scheduled rewards do not violate budgets or constraints at send time** – meaning if a reward is scheduled but later the budget changes or other factors, the system should re-validate when executing. Perhaps the budget is reserved at scheduling (deduct at schedule time to be safe) and if the reward is canceled before execution, add back the budget.
  - (This touches budget logic: an approach is to deduct budget when scheduled to prevent overallocation, and if canceled or expired not used, then credit back.)
- **FR 3.2.4 Personalized Messaging:** For each reward sent (single or bulk), the system shall allow the sender to include a **personalized message** to the recipient. This could be a custom note like “Thank you for your great work on Project X!” or “Happy Holidays, enjoy this token of appreciation.” In bulk sends, if personalization per recipient is desired beyond just name, the user would include those differences in the CSV (like a column for “Reason” that could be merged into the template). The platform should support at least basic personalization:
  - Placeholders for recipient name or other provided fields in the message template.
  - If the user is sending individually, they can write a unique message for that person.
  - The system shall include this message in the reward notification (email body or SMS text).
  - The message field should support plain text up to a reasonable length (e.g., 500 characters). Perhaps allow limited formatting (bold/italic or hyperlink) for email, but that might be advanced.
- **FR 3.2.5 Delivery via Multiple Channels:** The primary channel is Email, but the system shall support alternative delivery channels where applicable:
  - **Email:** Default method – the system sends an email to the recipient’s email address, containing either the reward details (like an e-gift card code or QR code) or a button/link to a redemption page. Emails should be branded (with the company’s name/logo if configured) and clearly state the reward information.
  - **SMS:** If a mobile number is provided and the reward type can be delivered via SMS (e.g., a short code or URL), the system should allow sending a text message with the reward link or code. This is useful when recipients respond better to text or if email is not available. The system may require integration with an SMS gateway and possibly limit SMS usage for short messages (since long messages or multiple could be problematic).
  - **In-App or Webhook-based:** For cases where the organization wants to deliver the reward within their own application interface, they might use the API to fetch the reward code and then display it in-app to the user (so the user sees it as part of their account on the company's app). This isn't exactly the system sending, but it’s a delivery method facilitated by the API. (We mention it to ensure our system can handle "no email send needed, just generate code and return to caller" if using API).
  - **Physical Delivery:** For physical rewards, the system will not directly deliver (since it's a shipping process), but it will initiate fulfillment. In terms of user-facing actions, if a physical item is selected, the system might either ask the sender to provide a shipping address for the recipient or send the recipient an email asking them to provide their address via a secure form. Then the item is shipped (likely by an external vendor or internal team). The system tracks this but it’s not an electronic channel like email/SMS. Still, the initial notification might still be email (like “We owe you a physical gift, click here to give us your address”).
  - **FR 3.2.5a:** The system’s design should be flexible to support adding other channels if needed (like messaging apps integration) though not in initial scope.
- **FR 3.2.6 Confirmation and Notifications:** When a user triggers reward delivery, the system shall provide appropriate confirmations:
  - After a single send, show a success message like “Your reward has been sent to [recipient email]” or if scheduled, “Your reward is scheduled to be sent on [date]”.
  - For bulk sends, possibly show “Rewards are being sent to X recipients. You will be notified when sending is complete.” and perhaps an on-screen summary (like how many queued).
  - If any errors occurred for some recipients in bulk, once done, show a summary: e.g., “Out of 500, 490 sent successfully, 10 failed. Click here to view details of failures.”
  - The system should also log this action in the audit log (with who sent what to whom and when).
  - Optionally, a user might opt to get an email confirmation or notification in the app that sending completed (especially for long-running bulk). E.g., send the manager an email “Your campaign XYZ distribution to 500 recipients has completed. 10 emails bounced.” but this can also be an in-app notification.
- **FR 3.2.7 Prevention of Duplicate Sends:** The system shall help avoid accidental duplicate sending of the same reward to the same recipient:
  - If a user accidentally tries to send the exact same reward to the same email within a short period, the system should either warn or prevent it (“This recipient already received the same reward recently. Are you sure you want to send again?”). This is to avoid spamming or double rewarding due to double-clicks.
  - At the very least, the UI will disable the send button after one click to avoid double submission.
  - In bulk import, if the list has duplicate emails, the system should either automatically de-duplicate or warn the user and skip duplicates.
  - These measures ensure a more polished experience and guard against certain user errors.
- **FR 3.2.8 Throttling and Batch Processing:** For very large bulk sends (e.g., thousands of recipients), the system shall send messages in batches to avoid overloading external services or being flagged as spam:
  - The platform might throttle sending to, say, 100 emails per minute if needed (depending on email provider guidelines) or as allowed.
  - Use of a background queue means the user doesn’t have to keep the browser open; the send will continue on the server side. The user can log out and it still goes.
  - The system should handle the queue robustly (if the app restarts, queued tasks persist, etc.).
  - Provide some status if possible in the UI for ongoing sends (maybe a progress bar or a refresh button to update status).
- **FR 3.2.9 Error Handling in Sending:** If something goes wrong during the sending process, the system shall handle it gracefully:
  - If the reward provider’s API fails to return a code (e.g., service down or out of stock), the system should retry a few times. If it still fails, mark that particular send as “Failed” and notify the user (for bulk, include in fail count). Possibly suggest a next step (“Try again later” or allow user to click resend once the issue is resolved).
  - If email sending fails for a particular recipient (e.g., email bounce due to invalid address), mark that reward’s status as **Undeliverable**. The system should surface this to the user, e.g., in the reward tracking list highlight in red, and allow the user to correct the address and resend (see tracking requirements).
  - The system must ensure that a failure for one recipient does not halt the whole bulk operation. It should isolate issues and continue with others.
  - If the entire sending service is unavailable (e.g., email API down), the system might queue and wait or after a certain time alert the user that sending is delayed. Possibly a system admin will intervene. For user perspective, they'd see pending status.
- **FR 3.2.10 Storing Delivery Info:** For each reward issuance (whether single or part of bulk), the system shall store the details of that "transaction":
  - Who initiated it (user id),
  - timestamp,
  - which reward (catalog item reference and value),
  - which recipient (email, maybe name),
  - any personalized message,
  - the send method (email vs SMS),
  - and any ID/reference from the provider (like if the provider returns an order ID or code, store it).
  - This data is crucial for tracking (Section 3.3) and for audit. It should be stored in the database such that it can be queried by status or campaign.
  - Sensitive details like the actual gift card code might be stored encrypted or not at all if not needed (for security), but typically we need to store it to display on redemption page if needed. We'll address that in security considerations.
- **FR 3.2.11 Support for Multi-Reward Bundles (Optional Advanced):** The system may allow sending **reward bundles** or choices in one go:
  - e.g., sending an email that offers the recipient a choice among multiple reward options (like "Pick either a $50 Amazon card or a $50 Target card").
  - If this is supported, in the send flow, the user would select multiple reward items and mark them as alternatives (as opposed to sending all to one person).
  - The system would generate a special redemption link that, when the recipient clicks, shows those options and lets them choose one. After one is chosen, the others become invalid for that recipient.
  - The sending record would note that multiple options were offered, and which one was ultimately redeemed. Budget handling might consider either reserving the highest amount or counting when redeemed.
  - This feature adds complexity but is a valuable feature (some platforms do this to increase recipient satisfaction).
  - Marking this as optional; if implemented, ensure tracking shows not just "Sent" but which one was picked at redemption.

In summary, the Reward Delivery feature must make it easy for authorized users to deliver rewards reliably and flexibly, whether one by one or at scale, immediately or scheduled, with personalized communications, while interfacing correctly with the underlying reward providers and communication channels. The success of this feature is judged by how intuitive the sending process is and how reliably recipients actually receive their rewards.

### 3.3 Reward Tracking and Lifecycle Management

**Description:** After rewards are sent, the platform will provide tools to track their status throughout the lifecycle (from creation to final redemption or closure). This feature is crucial for transparency and program management — product managers need to know which rewards have been claimed and which are still pending, and finance teams need to know which have been used (to account for actual expenses). Lifecycle tracking also helps identify issues (like failed deliveries or unredeemed rewards that might need reminders or follow-up).

The typical statuses a reward might go through include: _Initiated/Sent_, _Delivered_ (if we get confirmation of delivery, e.g., email delivered), _Opened_ (if we track that the email was opened or link clicked), _Redeemed_, _Expired_, _Cancelled_, _Failed_. Not all statuses apply to all scenarios (for example, “Delivered” could be skipped if we consider “Sent” as delivered unless bounce occurs). The system should present these statuses clearly to users and allow filtering and reporting by status.

Additionally, tracking involves enabling certain actions on rewards post-send, like resending a notification, canceling a pending reward (if possible), or manually marking something if needed.

**Functional Requirements:**

- **FR 3.3.1 Reward Status Tracking:** The system shall maintain a **status for each reward instance** (each reward sent to a specific recipient) and update it as it moves through the lifecycle. The statuses should include at least the following:

  - **Sent (or Pending Delivery):** The reward has been processed by the system and an attempt to deliver (email/SMS) has been made. This might be the initial status immediately after sending if we don’t yet know the delivery outcome.
  - **Delivered:** Confirmation that the reward notification reached the recipient. For email, “delivered” could mean we got a success response from the email server (i.e., not bounced). For SMS, that we got a delivery report. (We may or may not explicitly use this separate from Sent; possibly unify delivered with sent unless bounce indicates otherwise.)
  - **Opened:** If the platform includes tracking (like an email open tracker or the recipient clicked the redemption link), it can mark a reward as “Opened” when the recipient engages. This indicates the recipient is aware of the reward. Not all emails will be trackable (if images off, etc.), but clicking the link is a sure sign of open.
  - **Redeemed:** The ultimate success state. The reward has been redeemed/claimed by the recipient. For digital gift cards, redeemed might mean the user viewed the code on our site (which we treat as delivered to them) or if we have integration to know they actually used it at the vendor (rare for gift cards, but possible to check usage or just assume redeem when we delivered code). For physical items, redeemed might mean the recipient confirmed their address or we have delivered the package.
  - **Expired:** If a reward remains unredeemed beyond a defined period or by a set expiration date, it can be marked as expired. For example, a link valid for 3 months, after which the code is void or returned to pool. Expired means the recipient can no longer claim it. The system should support expiration rules (maybe configurable globally or per campaign).
  - **Cancelled:** If an admin/user proactively cancels a reward after sending but before redemption (for instance, they sent it mistakenly or the recipient is no longer eligible), they can cancel it. Cancelled typically means if the reward was not yet redeemed, it becomes invalid (we might attempt to revoke the code via provider if possible).
  - **Failed:** Indicates the reward could not be delivered or fulfilled. For example, if the gift card provider couldn’t provide a code (and we gave up after retries) or if an email is permanently undeliverable and no alternate contact, we might mark as failed. This is a terminal state meaning the intended delivery failed and won’t be automatically retried (without user intervention).

  The system shall present these statuses clearly (e.g., with labels or icons) and maintain timestamps for key events (when sent, when opened, when redeemed, etc.).

- **FR 3.3.2 Reward Dashboard/List:** The system shall provide a **Rewards Tracking Dashboard or List View** for users to monitor all rewards they have sent (or that their organization has sent, depending on permissions). This is typically a table or list of reward records with columns like:
  - Recipient (email or name),
  - Reward (name/value),
  - Date Sent,
  - Current Status,
  - and possibly Date Redeemed or Expiration.
  - There should be controls to filter this list by status (e.g., show only Pending/Unredeemed), by campaign, by date range, or by recipient (search by email).
  - This view lets a manager see at a glance how many are redeemed vs pending, etc., and drill down into details if needed.
  - If the organization has multiple managers, a manager might see only their own sent rewards by default, whereas an Admin or Finance could see all (filter by sender maybe).
- **FR 3.3.3 Status Updates:** The*(Continued from above)*

- **FR 3.3.3 Status Updates:** The system shall **automatically update reward statuses** based on events and feedback from integrated systems:
  - If an email bounce is received, update status to **Undeliverable/Failed** for that reward and log the bounce event (with timestamp and reason if available).
  - If the recipient clicks the redemption link, update status to **Redeemed** (or at least to Opened/Claimed if there are further steps to complete redemption).
  - If using certain gift card providers that allow querying redemption, the system should periodically check and update status to Redeemed when the card is actually used (if that info is accessible). (This may not be real-time for all providers, so we primarily rely on our own redemption portal events for status).
  - If a reward reaches its expiration date without redemption, update status to **Expired** at that time and ensure the code is invalidated (if possible via provider) or noted as expired.
  - These updates should trigger any relevant actions (e.g., if a reward is redeemed, remove it from “pending” lists).
- **FR 3.3.4 Manual Status Override:** The system shall allow authorized users (Org Admins, possibly Program Managers for their own campaigns) to **manually adjust a reward’s status** in special cases:
  - Example: Mark a reward as _Redeemed_ if the recipient claims they used it but perhaps not through our link (maybe they received code via phone call outside system and used it – edge case).
  - Example: Cancel a reward (change status to Cancelled) if needed after sending. Cancellation should ideally prevent redemption: if the code hasn’t been used, attempt to cancel it via provider or mark in system as void so if the link is clicked it shows “cancelled by sender”.
  - All manual changes should be recorded in audit logs (who did it, when, and what changed).
  - The UI might present these as actions like “Cancel reward” or “Mark as Redeemed” on a reward detail view, enabled only for those with permission.
- **FR 3.3.5 Resending and Reminders:** The system shall provide options to **resend reward notifications** or send reminders:
  - If a reward is in Undeliverable status due to an incorrect email, a user can correct the contact (edit recipient email) and trigger a **Resend**. The system will attempt delivery again (generate a new email, possibly a new reward link if security requires).
  - If a reward is pending (Sent but not redeemed) for a long time, a user may click “Send Reminder”. The system will send a follow-up email to the same recipient, referencing the reward and encouraging redemption. This should not create a new reward entry, just an additional notification, and should be recorded (maybe update a “last reminded” timestamp).
  - The system can also optionally automate reminders: e.g., an admin could configure “auto-remind after 7 days if not redeemed”. If implemented, the system shall send those automatically and mark that it sent a reminder.
  - After resending or reminding, keep the status as pending (unless it was undeliverable and now resent successfully, then mark as Sent/Delivered and pending redemption).
- **FR 3.3.6 Reward Detail View:** Users should be able to click on a specific reward entry in the tracking list to see a **detailed view**:
  - Show all info about that reward: recipient details, reward details, message sent, timestamps for each status change (Sent on X date, Opened on Y date, Redeemed on Z date, etc.), and if applicable the code or redemption link (perhaps masked for security if needed).
  - Show event history: e.g., “Email sent (delivered) at 10:00, Email opened at 10:05, Reward redeemed at 10:07 via IP 1.2.3.4” – whatever data is relevant.
  - Provide action buttons like Resend, Cancel, etc., on this detail view as appropriate given its current status.
  - Ensure sensitive info (like a gift code) is protected: maybe require clicking “Reveal code” with a confirmation if showing to an admin, to avoid shoulder-surfing issues.
- **FR 3.3.7 Aggregate Tracking Metrics:** The system shall aggregate reward statuses for summary displays:
  - For example, on a campaign overview page: “100 rewards sent, 80 redeemed (80%), 5 failed, 15 pending.”
  - Or on the dashboard: total pending vs redeemed across all programs.
  - While reporting (Section 3.8) will cover in-depth analytics, the tracking module itself might show counts or percentages to help users quickly gauge how things are going.
  - Filtered views (like if user filters the list by campaign or date) can show a summary of that subset (e.g., “Showing 50 rewards: 40 redeemed, 10 pending”).
- **FR 3.3.8 Budget Integration with Tracking:** The tracking system shall be aware of budget context:
  - Each reward entry knows which budget or campaign it was associated with. The tracking UI might allow filtering by budget or campaign (so a manager can see all rewards that counted against a particular budget).
  - When a reward is redeemed or cancelled, if the platform uses “spend on redemption” logic, it should notify the budget module to decrement or refund accordingly. (E.g., if budgets were only charged on redemption, then upon redemption event, mark that amount as actually spent.)
  - Conversely, if a reward expired or was cancelled unredeemed and the budget had been pre-deducted, the system could credit the budget (increase remaining by that value) automatically or flag it for admin to adjust. This process should be clearly defined to keep budget status accurate (discussed in 3.5).
- **FR 3.3.9 Data Retention in Tracking:** The system shall retain reward records for a configurable period (e.g., at least X years as required by company policy or indefinitely until manually archived).
  - However, for privacy, personal data within those records might be anonymized after a certain time if required (e.g., after 2 years, replace recipient email with a hash or “[redacted]” but keep the fact that a reward was sent and its status for aggregate stats). This ties to compliance requirements.
  - The system should allow exporting or archiving old records if needed to keep the main interface from being cluttered (maybe archive by year).
  - These considerations ensure the tracking module can handle a growing history without performance issues or privacy non-compliance.
- **FR 3.3.10 Notifications for Tracking Events:** Optionally, the system can notify users of certain events:
  - For example, an Admin might subscribe to be alerted if any reward fails (to address issues promptly), or if a high-value reward is redeemed.
  - A Program Manager might want a notification when all rewards in their campaign have been redeemed (or maybe when a particularly important recipient redeems).
  - This is an advanced feature and can be part of the notifications system (not core to functionality, but adds value). If implemented, it should be configurable per user or per campaign.

In summary, the tracking feature gives users visibility and control after sending rewards, ensuring that no reward “falls through the cracks.” It closes the loop on the reward process by showing who actually benefited from the incentives and highlighting any that did not reach the target or were not used, so users can act accordingly (send reminders, reallocate budget, etc.).

**Reward Lifecycle Status Definitions:** To clarify the statuses, here is a reference:

| **Status**               | **Description**                                                                                           | **Possible Transitions**                                                                                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Sent**                 | Reward issuance has been processed and notification is sent or in progress.                               | → Delivered (if confirmed) <br> → Undeliverable (if bounce) <br> → Opened (if detected) <br> → Redeemed                      |
| **Delivered**            | Notification reached recipient (no bounce). (Might be combined with Sent in practice).                    | → Opened <br> → Redeemed <br> → Expired                                                                                      |
| **Opened**               | Recipient opened the email or clicked the link (engaged).                                                 | → Redeemed <br> → Expired                                                                                                    |
| **Redeemed**             | Recipient claimed/used the reward. This is a terminal success state.                                      | (No further transitions; closed state)                                                                                       |
| **Undeliverable/Failed** | Delivery failed (email bounced or SMS failed, or provider error).                                         | → (User can update info and attempt Resend, which would create a new send attempt – effectively a new entry or reactivation) |
| **Cancelled**            | The reward was revoked/cancelled by an admin before redemption. Terminal state (recipient cannot redeem). | (No further transitions; closed)                                                                                             |
| **Expired**              | The reward was not redeemed within allowed time and is now expired (invalid). Terminal closed state.      | (No further transitions; closed)                                                                                             |

_Table 3.3:_ Reward status definitions and transitions. (Note: Not every reward will go through all these; e.g., some may go straight from Sent to Redeemed without an Opened status if we don't track opens explicitly.)

### 3.4 Reward Redemption Process and Recipient Experience

**Description:** The Reward Redemption process refers to how recipients (employees, customers, partners, etc.) actually claim and use the rewards they've been sent. This involves the user experience on the recipient side, such as receiving an email or text, clicking a link, and being guided through obtaining their reward (like seeing a gift card code or confirming shipping for a physical item). Ensuring a smooth and simple redemption process is critical, as it directly impacts the satisfaction of the end recipients and the credibility of the reward program.

This section covers requirements for what happens from the moment a recipient is notified of their reward to the point where they successfully redeem it. It also covers error handling from the recipient’s perspective (like what if the link doesn't work or they have questions) and how the system handles redemption in various scenarios.

**Functional Requirements:**

- **FR 3.4.1 Reward Notification to Recipient:** When a reward is sent, the system generates a **notification to the recipient**. Typically this is an email (or SMS, as allowed). Requirements for the content and format:
  - It shall clearly identify the sender (the company or person who sent the reward) – e.g., using the company’s name/logo in the email and a friendly from-name like “Acme Rewards Team”.
  - It shall have a clear subject line, e.g., “You’ve received a reward from [Company]!” to ensure the recipient recognizes it's something positive and not spam.
  - The message shall include the personalized note from the sender (if provided), or a default message if none (like “Congratulations, here is your reward!”).
  - It shall clearly state what the reward is or how to get it – typically via a prominent **call-to-action** (CTA) button or link, such as “Claim Your Reward”.
  - For digital gift cards, the email might either contain the redemption code directly or (more securely) a button “View Your Gift Card” which leads to the redemption page where the code is revealed (the latter allows tracking and perhaps choice).
  - For rewards that offer a choice, the email should explain that and direct them to the page to choose.
  - For physical rewards, the email could say “Please provide your address to receive your gift” with a link to a form.
  - The email should include contact info or support link in case the recipient has issues (like a line: “For questions, contact rewards@company.com”).
  - **Unsubscribe/Opt-out link:** if required by law (e.g., CAN-SPAM), though if this is a one-time transactional email related to an action the user took, it might not need an unsubscribe. However, to be safe and polite, if we anticipate multiple reward emails, we might include an option “Don't want to receive further rewards emails? Click here” which would notify the company (this touches compliance).
- **FR 3.4.2 Secure Redemption Link:** The email/notification shall contain a **secure redemption link** (or unique code) for the reward:
  - If using a link, it should be unique to the reward and contain a secure token (a long random identifier) so that only someone with that link can redeem the specific reward.
  - The link URL likely points to our platform’s redemption page (e.g., https://rewards.incentivehub.com/claim/ABC123XYZ).
  - The link token should be one-time use: once the reward is marked redeemed, further visits should either show “already redeemed” or be disabled.
  - The system should ensure these links cannot be easily guessed or forged. Use HTTPS for all such links.
  - If the reward is delivered by code in the email (not using a link), ensure the code is not easily reused maliciously (in that scenario, it's up to the gift card provider’s security).
  - Optionally, the platform could allow adding an extra verification step for high-value rewards (like ask the recipient to enter their email or last name on the redemption page to confirm identity). But this can add friction, so probably not unless necessary.
- **FR 3.4.3 Redemption Web Page:** When the recipient clicks the link in their notification, the system shall present a **Redemption Page** in their browser (mobile or desktop compatible). Requirements for this page:
  - It should be branded with the sending company’s logo or name (which the platform can use from the org settings) to reassure recipients.
  - It should greet the recipient, possibly by name if we have it (e.g., “Hi John, you have received a $50 Gift Card!”).
  - The page content depends on reward type:
    - For a **single gift card reward**: The page should prominently display the reward details. If we require an extra click “Reveal Code” (for security/tracking), then a button does that and then shows the code (and maybe instructions: “Use this code at checkout on Amazon.com”). We might show an image of the gift card or the brand logo as well.
    - If the code is shown, provide a “Copy Code” button for convenience.
    - For a **multi-option reward**: The page should list the options (with perhaps radio buttons or tiles to select). E.g., “Choose your reward: ( ) $50 Amazon Card ( ) $50 Target Card ( ) $50 Walmart Card”. The user selects one and clicks “Claim” or “Submit”, which then shows them the details for the chosen one (and locks out the others).
    - For a **physical reward**: The page should either ask for shipping address if not predetermined. Fields for name, street, city, etc., with a submit. Possibly pre-fill if we have some info (rarely we would for external recipients). After they submit address, show confirmation “Thank you, your item will be shipped to the address provided. You’ll receive it in X days.” The system marks reward as redeemed at that point (and possibly triggers fulfillment).
    - For **other types**: Adjust accordingly. E.g., if it’s a discount code for the company’s service, the page might show the promo code and how to use it (“Enter this code on our website to get your discount.”).
  - The redemption page must be mobile-friendly (large buttons, vertical layout on small screens).
  - It should also have a help link or contact info in case the user has trouble (“Need help? Contact support…”).
  - The page should handle the case if the link is invalid or already redeemed:
    - If token not found or invalid: show an error like “This reward link is invalid. It may have been entered incorrectly or expired.”
    - If already redeemed: “This reward has already been redeemed on [date]. If you believe this is an error, contact support.”
  - After successful redemption, the page can show a nice confirmation message or animation (for good UX, e.g., confetti animation or big “Thank you!”).
  - If the reward is something like points or an account credit without a code, the page might just say “Your account will be credited with $X within Y days” and that's it.
- **FR 3.4.4 Account-Free Experience:** The recipient should **not be required to log in** or create an account on our platform to redeem a typical reward. The unique link serves as authentication. (The only exception might be if a company chooses to require their employees to log in via SSO to claim internal rewards for security, but that would be a special configuration.)
  - Thus, all redemption pages must be accessible with just the token (and maybe a simple verification if needed).
- **FR 3.4.5 Error Handling on Redemption:** The system shall handle common errors a recipient might encounter:
  - If the redemption link is expired or invalid, display a user-friendly message as described above. Possibly include a contact or an option to request a new link (which would notify the sender).
  - If the link was already used, clearly state it and perhaps who used it if that makes sense (though usually just say already redeemed).
  - If the recipient tries to choose a reward option but that option is no longer available (maybe one option stock ran out just at that moment), the system should inform them and ideally still fulfill with an alternative. (We would try to avoid offering something out of stock in the first place).
  - If a physical address validation fails (invalid address format), prompt them to correct it.
  - Essentially, any error should yield a message and not just break silently.
- **FR 3.4.6 Security and Fraud Prevention:** The redemption process should include measures to prevent abuse:
  - The unique token in link is primary. Additionally, rate-limit attempts (if someone tries to brute force tokens, rate limit requests from an IP).
  - Possibly tie a token to the recipient’s email (we have their email, so if someone tries a token and enters a different email in a form, maybe warn or disallow unless it matches our record).
  - For very sensitive rewards, optionally allow an OTP or email verification: e.g., send a verification code to the recipient’s email or phone to enter on the site to confirm identity. This is probably unnecessary for most use cases and would be optional.
  - Monitor if a token has multiple redemption attempts with wrong info (could signal someone forwarded their link; but since link itself is enough, not much to input incorrectly).
  - Ensure the redemption pages and any form are served over TLS and that no sensitive info persists client-side after.
- **FR 3.4.7 Acknowledgment to Sender (optional):** The platform may send a notification back to the sender when a reward is redeemed (if they want to know). For instance, a setting could allow “Email me when the recipient redeems the reward.” If enabled, when John Doe redeems, the Product Manager gets an email: “Your reward to John Doe was redeemed on [date].” This closes the loop for the sender. It’s optional per user or campaign basis.
- **FR 3.4.8 Redemption of Multi-Choice Rewards:** If a reward allowed the recipient to choose one of multiple options:
  - Once the recipient picks one and confirms, the system shall mark the chosen one’s reward instance as Redeemed for that person and immediately invalidate the other options’ codes (if codes were pre-fetched) or simply note they weren’t used.
  - If possible, the system could recycle the unused codes (e.g., return them to inventory or cancel them via provider to avoid cost). That depends on provider capabilities.
  - Ensure the recipient cannot go back and choose another (block the link after first submission).
  - The confirmation page should then detail the one they chose (“You selected: $50 Amazon Gift Card. Your code is: ...”).
- **FR 3.4.9 Support for Various Browsers/Devices (UX):** The redemption process shall be tested to work on common browsers and on mobile devices, since recipients might click on their phone or at work on IE/Edge, etc. (This ties to non-functional compatibility requirements but is mentioned to highlight user experience).
- **FR 3.4.10 Accessibility for Recipients:** The redemption page should be accessible (e.g., screen-reader friendly) as some recipients may have disabilities. Ensure that the CTA buttons are properly labeled, etc., so everyone can redeem their reward.
- **FR 3.4.11 Post-Redemption Communication:** After redemption, if appropriate, the system might send the recipient a follow-up email confirmation or copy of the reward details:
  - For example, if on the web page they saw a code, also email them “Here is your gift card code again for your records.”
  - Or if they entered address for a physical gift, maybe email them “We received your address and will ship your gift to you by X date. Thank you!”
  - This is a good practice to provide extra assurance and record.
  - Make this configurable; some may not want double emails.
- **FR 3.4.12 Recipient Opt-Out:** If a recipient really does not want to receive these incentives (some might consider it spam), provide a way to opt out of future rewards from that company:
  - Perhaps an unsubscribe link in the footer of emails as mentioned. Clicking it could mark that email on a suppression list for that organization.
  - If so, the platform should respect this by warning senders if they attempt to send a reward to an opted-out recipient (“This recipient has opted out of reward emails. You cannot send unless they consent again.”).
  - This ensures compliance with the recipient's wishes.

In essence, the redemption process should be **easy, quick, and reliable** for recipients. They shouldn’t have to struggle or wonder how to get their reward. Any confusion or failure here can sour the goodwill the reward was meant to generate. Hence, these requirements emphasize clarity, security, and user-friendliness in the recipient experience.

### 3.5 Budget Management

**Description:** Budget Management features enable organizations to control and monitor how much is being spent on rewards. Since incentives often come from a marketing or HR budget, it’s crucial to set limits (so you don’t overspend) and track spending in real time. The platform will allow admins or finance roles to define budgets for specific scopes (e.g., an annual budget for the whole company’s rewards, or separate budgets per team, campaign, or project) and then track all rewards against those budgets. It will enforce rules like preventing sends that would exceed the budget or requiring approvals for exceptions.

The budget module also includes the ability to view remaining funds, see breakdowns of spending, and adjust budgets. Integration with reporting is strong here, as well as potentially integration with finance systems (for invoicing or cost center mapping).

**Functional Requirements:**

- **FR 3.5.1 Define Budgets:** The system shall allow authorized users (Org Admin or Finance Manager roles) to **create and configure budgets** for reward programs. Key elements:
  - **Name and Purpose:** A budget should have a name and optional description (e.g., “FY2025 Sales Incentives Budget”).
  - **Time Period:** Optionally define a start and end date for the budget (e.g., Q1 2025, or full year 2025). Budgets can be ongoing or time-bound.
  - **Amount:** The total amount allocated (in the org’s base currency). E.g., $10,000.
  - **Scope of Budget:** Determine what this budget applies to. Some possible scopes:
    - _Global/General Budget:_ applies to all reward spending (if the org has one pot of money).
    - _Campaign/Program-specific:_ e.g., a budget specifically for a particular campaign or use case. Then when sending, the user would tag the send to that campaign/budget.
    - _Department or Team:_ e.g., Marketing has $X, Sales has $Y.
    - _User-specific:_ possibly allocate sub-budgets to particular managers (“each manager gets $1000 to spend per quarter”).
    - The system should support at least one level of categorization (project or campaign budgets under a master budget, etc.). For initial scope, even one level (multiple named budgets that the sender can choose from) would work.
  - **Currency:** Budgets will be tracked in one currency (the org’s base currency set in org settings). If rewards are in other currencies, the system will convert their cost to this base for budget accounting (using conversion rates).
  - **Approval Threshold:** Optionally, a budget can have a rule that any single reward above a certain value or any send that exceeds the remaining budget requires approval. (This might be a global setting too, but could be per budget).
  - **Owners/Approvers:** Possibly assign who can approve or who is notified of budget issues.
  - **Notifications:** Settings if any (like “notify me at 80% utilization”).
- **FR 3.5.2 Associate Spending with Budgets:** The system shall ensure every reward sent is **linked to a budget**. How:
  - If there is only one default budget, all spending goes to it automatically.
  - If multiple budgets exist, when a user initiates a send or campaign, they must select which budget it falls under (the UI could default based on campaign settings or user’s department).
  - The reward record then stores a reference to that budget, and the budget’s remaining amount is decremented by the reward value (depending on accounting method, either immediately or on redemption, see below).
  - For bulk sends, all in that batch typically use the same budget selected.
  - If a user doesn’t have permission to use certain budgets (maybe each manager only sees their budget), the UI/API should enforce that (only list budgets available to them).
  - The platform should also allow splitting budgets for complex cases (like half cost from one budget, half from another) – this is advanced and likely not needed initially. We can assume one reward draw from one budget.
- **FR 3.5.3 Budget Limit Enforcement:** The system shall **enforce budget limits** in real-time to prevent overspending:
  - When a user attempts to send a reward or schedule one, the system will calculate the total cost of that action and compare it to the available balance of the chosen budget.
  - If the cost would cause the budget’s used amount to exceed its total:
    - If the user has no override rights, the system shall block the action and inform the user (“This action would exceed the budget limit of $X. Please adjust the reward amount or request a budget increase.”).
    - If an approval workflow is in place, the system might instead allow the user to submit the request, but mark it as “Pending Approval” (the actual send won’t happen until an approver okays it).
    - If an admin (who might have override ability) is doing it, maybe just warn but allow if their role permits exceeding budgets (or typically even admins should set proper budgets rather than exceed).
  - The point is to never automatically overspend a set budget without human sign-off.
- **FR 3.5.4 Budget Deduction and Restoration:** The system shall update the **budget balances** as rewards are sent and resolved:
  - **Deduct on Send vs Redeem:** We need to decide policy. Two main approaches:
    1. Deduct the budget at the time of sending (treat the money as committed once reward is sent). If later the reward is not redeemed and gets cancelled/expired, the system could credit the budget back.
    2. Deduct the budget only when a reward is redeemed (so you don’t count those that never get used).
    - Approach 1 is simpler and safer to ensure you don’t accidentally send more codes than you budgeted. Approach 2 can optimize usage but complicates tracking.
    - Possibly allow configuration of which accounting method. Many likely use deduct on send for simplicity.
  - The system shall implement one of these consistently and document it in the UI for clarity (“Budgets track sent value” or “Budgets track redeemed value”).
  - If deducting on send:
    - Immediately subtract the reward’s face value from the budget’s remaining pool when sending.
    - If that reward later is cancelled or expires unused, the system shall add that value back to the budget (making it available again). This should probably require confirmation by an admin or automatic if we are certain no cost incurred (like an unused gift card might be refundable or not charged).
    - Implementation: when marking reward Expired, if not redeemed, do a budget increment.
  - If deducting on redeem:
    - When a reward is sent, mark that portion of budget as “committed” but not “spent”. This could be just a conceptual thing (maybe show committed vs actually spent).
    - Only when redeemed event occurs do we decrement the budget balance.
    - If reward expires unredeemed, then that committed amount is released (so remaining budget goes back up or the committed portion is removed).
  - In either case, the system must handle concurrency so two sends at same time still update budget correctly (transactions/locking).
  - The budget record should track at least: total, used amount, and optionally committed amount if using that concept, and remaining (which could be total - used under send mode, or total - committed under redeem mode).
- **FR 3.5.5 Budget Dashboard:** The platform shall provide a **Budget Management interface**:
  - A list of budgets with key info: Name, Total Amount, Amount Spent (or committed), Remaining Amount, and % used. Possibly a simple bar indicator of usage.
  - The ability to click on a budget to see details: including a log of all transactions (rewards sent, possibly with references to reward IDs or campaign names, amounts, dates).
  - Filtering those transactions by date or campaign might be useful here or in reports.
  - It should also show any pending approval requests related to that budget (like if someone attempted an overspend pending approval).
  - If budgets have time periods, indicate if it’s active or expired (e.g., a Q1 budget after March 31 might be closed).
  - If budgets auto-renew or have phases, possibly show next period’s budget (maybe out of scope to automate recurring budgets in v1; could just clone budgets for each period manually).
- **FR 3.5.6 Modify Budgets:** Authorized users shall be able to **modify budget settings**:
  - Increase or decrease the total allocated amount (with appropriate audit logging). If decreased below current spent, disallow or warn.
  - Extend or change the time period (e.g., extend an end date).
  - Enable or disable (freeze) a budget – e.g., if a budget is on hold, the system could prevent further use without deleting it.
  - If a budget is no longer needed, maybe mark it archived – not used for new sends but still in reports for historical spend.
  - Option to transfer remaining funds from one budget to another (nice-to-have for end of year, etc.). If not direct, users can manually adjust amounts.
- **FR 3.5.7 Multi-Level Budgets & Approvals (Advanced):** In some organizations, there might be hierarchical budgets:
  - E.g., an overall company budget and then departmental sub-budgets. Or a manager has a personal quota which rolls up to department total.
  - The system could support linking budgets (so spend counts against both the sub and the master). This adds complexity and might be phase 2.
  - For now, likely handle one level at a time (the admin will ensure the sum of all sub-budgets equals the master manually).
  - Approvals: The system shall allow an approval workflow if configured (particularly for overspend):
    - If a user tries to send that exceeds budget or a single reward over a threshold, instead of outright blocking, system can trigger an approval request to a Finance Manager or Org Admin.
    - That approver can be notified (by email or in-app notification), and can approve or deny via the interface.
    - If approved, the action proceeds (either immediately sends the reward if it was waiting, or allows the user to resend now that it’s approved).
    - If denied, inform the requester and do not send.
    - All this with timestamps and logs.
    - This workflow needs UI screens to list pending approvals for approvers.
    - Approvals can also be used for large campaigns (“I want to send 1000 rewards costing $50k, require CFO approval”).
    - [This is a complex feature; depending on priorities, might be simplified or deferred. The SRS acknowledges it as a need for some clients.]
- **FR 3.5.8 Real-Time Budget Feedback:** The UI should give immediate feedback on spend when users are setting up a send:
  - E.g., if they select 100 recipients and a $20 reward, and choose a budget, the interface might show “Total cost: $2000. Remaining budget after send: $500 (of $2500)” to make them aware.
  - If that would go negative, maybe highlight in red even before they click send, to encourage adjusting or seeking approval.
- **FR 3.5.9 Linking to Accounting:** (Optional integration) Some companies might want to map budgets to internal accounting codes or cost centers.
  - The system could allow entering an Accounting Code for each budget and include that in reports or exports, so finance can tie expenses to their system.
  - If integrated with an ERP, perhaps export a summary of rewards spent per budget for import into their financial system, but direct integration not likely in v1.
- **FR 3.5.10 Notification of Budget Status:** The system shall support notifications for budget thresholds:
  - For example, when a budget’s used amount exceeds 80% of total, send an email to the budget owner: “Budget X is 80% utilized.”
  - Similarly, if fully used (or attempted use beyond limit), alert relevant people.
  - If budgets expire at period end, maybe alert if money is left (“Budget Y period ending with $500 unused” – some might want to use it or at least know).
  - These rules could be configurable (set threshold percentage or absolutely, choose recipients of these alerts).
- **FR 3.5.11 Handling Multi-Currency:** If an organization operates with budgets in one currency but sends rewards in another:
  - The system shall convert the cost of a reward to the budget’s currency for accounting. Use up-to-date exchange rates (fetched daily or provided by admin).
  - Possibly allow setting a static rate if needed (some finance might want to use a fixed rate for budgeting).
  - Show conversion on relevant screens (e.g., “This €50 reward will count as $55 against your budget”).
  - For simplicity, might require budgets in one currency only, and require that as base for all.
- **FR 3.5.12 Historical and Future Budgets:** The system should keep budgets from past periods for record (don’t delete them when period over, they are needed for auditing spend).
  - Also allow setting up future budgets (e.g., next year’s budget, which might be inactive until start date).
  - At a period turnover, it might automatically start using the new period’s budget if configured (if not, admin just switches which one is active).

Overall, budget management ensures that those controlling the purse have oversight and control over reward spending, preventing surprises or runaway costs. It introduces necessary checks and balances (like approvals) into the process of sending rewards, which is crucial in an enterprise setting.

### 3.6 User Management and Role-Based Access Control

**Description:** User Management and RBAC features govern how different users access and interact with the platform. In a SaaS platform used by organizations, it's essential to have a robust system for creating user accounts, assigning roles with specific permissions, and managing these accounts (passwords, SSO, activation/deactivation, etc.). Role-Based Access Control means each role (like Admin, Manager, Finance, Viewer) has a defined set of allowed actions, and the system will enforce those permissions for every operation.

This section describes how user accounts are handled, how roles and permissions are structured, and what administrative functions exist for managing users and their access rights.

**Functional Requirements:**

- **FR 3.6.1 User Account Creation:** The system shall allow Org Admins (and platform super-admins) to **create new user accounts** for their organization.
  - Via an “Invite User” function: Admin enters the person’s name, email, and selects a role. The system sends an invitation email to that address with a sign-up link.
  - The invite link allows the user to set their password (if using platform auth) or to confirm and log in if using SSO (if SSO, maybe just adds them directly once they use SSO).
  - Alternatively, Admin can directly create an account with a temporary password and convey it out-of-band (less secure, invitation is preferred).
  - The system should validate that the email is not already in use (within that org or globally, as appropriate – typically email + org unique).
  - Possibly allow adding a user to multiple roles or groups if needed (initial assumption: one primary role per user).
- **FR 3.6.2 Role Assignment:** The system shall allow Org Admins to assign a role to each user (and change it later).
  - The default roles provided: Org Admin, Program/Rewards Manager, Finance Manager, Viewer (as described in Section 2.3).
  - The system should enforce that at least one Org Admin exists (so you can't remove admin rights from the last admin).
  - Roles determine which sections of the UI the user can access and which actions they can perform.
  - Possibly allow custom roles in the future, but not required in initial version if the predefined cover the bases.
- **FR 3.6.3 Permissions Matrix Enforcement:** The system shall enforce permissions for various actions based on role:
  - Only Org Admins can manage users, roles, global settings, and view all data.
  - Program Managers can create/send rewards and campaigns, view the results of their own programs (and possibly others if allowed).
  - Finance Managers can see all financial info (budgets, spend reports), manage budgets, approve expenses, but may not initiate reward sends (or maybe they can, depending on configuration).
  - Viewers can only see certain dashboards or reports, without the ability to change anything.
  - These rules must be enforced both in the UI (don’t show buttons they can’t use) and on the server side (API checks).
  - Example: If a Viewer tries to call an API to send a reward, the server returns an authorization error.
  - The specific mapping of privileges to roles should be documented (see Table 3.6.1 below for typical mapping).
- **FR 3.6.4 Single Sign-On (SSO) Integration:** The system shall support SSO for user authentication (this is often a requirement for enterprise clients).
  - Org Admins should be able to configure SSO for their organization by providing necessary metadata (like uploading SAML IdP details or enabling OAuth integration).
  - If SSO is enabled, users from that org will log in via the corporate IdP. New user accounts might be provisioned automatically on first successful SSO login (Just-In-Time provisioning) if they don’t exist, possibly with a default role or no access until an admin assigns (configurable).
  - The platform must ensure RBAC still applies after SSO (SSO just handles identity, not authorization levels; possibly we can map an IdP attribute to a role if such info is provided).
  - Non-SSO (local login) should still be available if SSO is not configured or for certain accounts. Possibly allow both (some smaller clients will just use username/password).
- **FR 3.6.5 Authentication and Security:** The system shall implement secure authentication practices:
  - If using local login: enforce strong password policy (minimum length, complexity, etc., configurable). Hash passwords (e.g., bcrypt).
  - Implement “Forgot Password” flow: user can request a reset link emailed to them, which lets them set a new password securely.
  - Optionally, support two-factor authentication for local logins (especially for Org Admin accounts). Possibly an out-of-scope advanced feature, but mention if needed by compliance.
  - Maintain session security (use secure cookies or JWTs with proper expiration).
- **FR 3.6.6 User Profile Management:** Users should be able to manage their own profile:
  - Change their display name.
  - Change password (if local auth).
  - Set preferences (like notification preferences, language preference for UI, etc.).
  - View their own recent activity (maybe last login, etc., mostly for security awareness).
- **FR 3.6.7 User Deactivation/Deletion:** Org Admins shall be able to **deactivate** a user account (prevent login) or delete it if an employee leaves the company.
  - Deactivation keeps their historical actions (so their sent rewards still show who the sender was but that user can’t login).
  - Deletion might anonymize or remove personal info but likely we'd rarely truly delete; better to deactivate to retain history (perhaps with an option to scrub personal data for compliance after X time).
  - When an account is deactivated, any pending actions assigned to them (like approvals) should be reassigned to an admin or appropriate fallback.
  - If a user is the sole owner of something (like budget owner) and is removed, system should prompt to transfer those responsibilities to another user.
- **FR 3.6.8 Audit and Monitoring of User Activities:** The system shall log important user management events:
  - Creating a user, deleting/deactivating, role changes, password resets (not the new password, just the fact of reset), SSO configuration changes, login attempts (especially failures for security).
  - Some of this overlaps with audit logging (Section 3.7) but included here to highlight user-related events.
- **FR 3.6.9 Access Control in UI:** The UI shall dynamically adjust to the user's role:
  - Non-admins should not see the “Administration” section for user management or global settings.
  - Finance might see budgets and reports tabs, whereas a normal Manager might not see finance reports.
  - Attempting to navigate directly to an unauthorized page (via URL manipulation) should result in an access denied page.
  - This provides a cleaner experience and additional security.
- **FR 3.6.10 Support Platform Admin (Superuser):** Outside of client orgs, there are platform-level admins (our company’s support staff) who need full access to manage any org, help troubleshoot, and manage global catalog.
  - The system shall have a super-admin role that can impersonate an org admin or access any tenant’s data when needed (for support). This is extremely sensitive and should only be internal.
  - Possibly require an extra confirmation to use impersonation and log it in audit (to track support staff actions).
  - This ensures we can support clients but is not exposed to normal users.
- **FR 3.6.11 Groups/Teams (Optional Future):** Perhaps support grouping users into teams with shared access. For example, multiple managers in Marketing who can all see each other’s campaigns if needed. This can be done via sharing campaign access rather than roles. Not needed in initial scope beyond what roles already cover (everyone in Manager role could see all campaigns, or restrict to own – this is a design decision).
- **FR 3.6.12 License Counts (if any):** If we decide to enforce a limit on number of user accounts per org (some SaaS plans do that), the system should track how many users an org has and not allow creating beyond limit or warn them. Since not mentioned explicitly, likely unlimited users or controlled by contract, so maybe not needed to enforce in software.

**Table 3.6.1 - Role Permissions Summary:**

| **Feature / Action**               |         **Org Admin**         |                 **Program Manager**                 |          **Finance Manager**           |           **Viewer**           |
| ---------------------------------- | :---------------------------: | :-------------------------------------------------: | :------------------------------------: | :----------------------------: |
| Manage Users (invite/remove)       |              Yes              |                         No                          |                   No                   |               No               |
| Configure Org Settings (SSO, etc.) |              Yes              |                         No                          |                   No                   |               No               |
| Create/Edit Budgets                |              Yes              |           Possibly (no, or propose only)            |                  Yes                   |               No               |
| Approve Budget Exceptions          |              Yes              |                  No (request only)                  |          Yes (if designated)           |               No               |
| Send Rewards (single/bulk)         |           Yes (any)           |                  Yes (their scope)                  |     Generally No (not their role)      |               No               |
| Schedule/Cancel Rewards            |           Yes (any)           |                Yes (their own sends)                |                   No                   |               No               |
| View Own Campaign Stats            |           Yes (all)           |                Yes (their campaigns)                | Yes (all, if finance focuses on spend) |       Maybe (if shared)        |
| View All Campaigns/Rewards         |              Yes              | Possibly (if allowed by admin, or only within dept) |    Yes (especially financial data)     | Limited (perhaps summary only) |
| Manage Catalog (custom rewards)    |              Yes              |        Maybe (if allowed to add suggestions)        |                   No                   |               No               |
| Access Reports/Analytics           |          Yes (full)           |  Yes (for their data; maybe all if not sensitive)   |     Yes (especially spend reports)     | Yes (read-only, maybe limited) |
| Audit Log Access                   |        Yes (org-level)        |                         No                          |    Perhaps limited (their actions)     |               No               |
| Impersonate Users                  | No (only platform superadmin) |                         No                          |                   No                   |               No               |

_(This table can be adjusted per organizational needs; it's an example of typical separations.)_

In conclusion, the User Management and RBAC system ensures that each user of the platform has appropriate access and capabilities, aligning with their role in the organization’s reward program process. This prevents unauthorized actions and simplifies the UI for each role by showing them only what they need.

### 3.7 Audit Logging

**Description:** Audit Logging is a critical feature for security, compliance, and internal accountability. It involves recording a detailed, tamper-evident log of important events and actions that occur in the system. For a rewards platform, this means tracking things like user logins, changes to configurations, creation or sending of rewards, budget modifications, etc., along with who performed the action and when. This allows administrators to review actions (especially destructive or financial ones), and it supports compliance requirements (like SOC 2's requirement for audit trails).

This section specifies what events should be logged and what capabilities exist to view or export those logs.

**Functional Requirements:**

- **FR 3.7.1 Events to Log:** The system shall capture audit log entries for significant events including, but not limited to:
  - **User Authentication Events:** Successful logins (with user identity, timestamp, and source IP/device if possible), failed login attempts (with reason like wrong password, account locked), logout (if tracked).
  - **User Management Events:** User created, role changed, user deactivated or deleted, password reset (initiated and completed), SSO configuration changes or activation.
  - **Permission/Settings Changes:** Any changes in organization settings (like turning on SSO, changing email templates, toggling a feature).
  - **Budget Events:** Budget creation, modification (amount or time changed), deletion, and any approvals of budget overrides.
  - **Reward Lifecycle Events:** Reward send initiated (with details such as sender, recipient, reward type, value, budget used), reward cancelled by user, reward code viewed (maybe for auditing if needed), reward marked redeemed (especially if done manually by an admin for some reason).
  - **Integration Events:** Changing API keys or webhook endpoints in integration settings, if relevant.
  - Basically, any admin-level action or system-level important occurrence should be logged.
- **FR 3.7.2 Log Details:** Each audit log entry shall include:
  - Date and time (with timezone or in UTC).
  - The actor (which user or system process performed the action). Use a unique identifier (user ID and name/role, or "System" for automated events).
  - The action performed (e.g., "User Login", "Created Budget", "Sent Reward", "Changed Role", "System Error").
  - Context or target of the action:
    - For example, if "Sent Reward", log the Reward ID or details (like “Sent $50 Amazon gift to john@example.com”).
    - If "Changed Role", mention which user’s role changed and from what to what.
    - If "Budget Modified", mention budget name and old vs new amount if applicable.
  - Outcome or status: e.g., "Success", "Failed", "Denied". (For login attempts and such.)
  - Perhaps IP address for security events like login.
  - A unique ID for the log entry itself.
- **FR 3.7.3 Read/Export of Logs:** Org Admins (and only them, by default) shall have the ability to **view audit logs** for their organization.
  - Provide an Audit Log page or tab listing entries in reverse chronological order.
  - Filters to narrow by date range, by user, or by event type would be helpful (e.g., show me all role changes in last month).
  - Searching by keyword (e.g., a user’s email to see all actions by them).
  - The interface should display the entries with meaningful description (e.g., "Jan 5, 2025 14:32: Admin Alice created user bob@company.com with role Viewer").
  - Provide an option to **export** the audit log to CSV for an interval (for offline analysis or compliance archival).
  - Ensure exported logs include all detail and are properly formatted.
  - If logs are extremely lengthy, consider pagination or requiring filters to avoid browser overload.
- **FR 3.7.4 Integrity and Security of Logs:** Audit logs are sensitive (they record possibly security-related actions) and must be protected:
  - Ensure only authorized roles (Org Admins, and platform super-admins for all orgs) can view them. Even Program or Finance Managers typically should not see audit logs (unless company grants that specifically).
  - The logs should be stored in a tamper-resistant way. At a minimum, no one except maybe platform DB admins can modify them, and any attempt to alter logs (if an admin function existed) should itself generate an audit entry.
  - Possibly implement append-only storage (so even an Org Admin cannot edit logs via the UI).
  - Consider log retention policies: default keep for X years. If needed for compliance, allow exporting and deleting older to save space, but likely we keep them since text logs don’t take too much space for normal usage.
  - Platform super-admin should be able to access logs of any org for support, but those actions (viewing logs of an org) might be logged too as part of platform logs.
- **FR 3.7.5 Audit Log of Reward Events vs User Events:** Note that some reward events (like "Reward Redeemed") may also be captured in the Reward Tracking and not necessarily duplicated in audit logs for Org Admins. However, for completeness, it’s fine if there's overlap.
  - We should ensure critical financial events (like "Reward of $X redeemed") are indeed logged somewhere accessible to admin (maybe both in tracking UI and audit log).
- **FR 3.7.6 System Audit for Compliance (Platform-Level):** (This might be more internal than part of product features visible to Org Admins) The system should maintain platform-wide logs to meet compliance (like tracking platform admin actions, or if configuration was changed by developers).
  - This likely is handled outside the web app (like cloud logs), but mentioning in SRS that audit logging design will consider compliance requirements beyond just tenant-level logs.
- **FR 3.7.7 Notification on Sensitive Actions:** Optionally, the system might generate alerts for certain audit events:
  - E.g., notify Org Admin if a new Org Admin is added (in case it wasn’t them, could be misuse).
  - Notify if someone attempts repeated failed logins (security concern).
  - These can tie into security monitoring more than product feature, but could be offered as configurable alerts to super admin.
- **FR 3.7.8 Privacy in Logs:** Ensure not to log sensitive personal data in audit entries unnecessary:
  - E.g., don’t log raw passwords (never), don’t log an API key in plain text if someone enters it (mask it).
  - If a user triggers sending a reward, logging “to john@example.com” is fine since that email is in system anyway. But be mindful of any privacy requests (like if John used right to be forgotten, maybe we should pseudonymize his email in logs too).
  - Typically audit logs are exempt from deletion requirements for a period because they're needed for legal compliance (they often can keep some personal identifiers as legitimate interest for security), but it's something to mention under compliance that we handle appropriately.

Audit logging ensures traceability. If a question arises like “Who gave this partner a $500 gift without approval?” or “How did this user become an admin?”, the audit log will have the answer. This fosters trust and accountability and is often mandated by corporate IT policies.

### 3.8 Reporting and Analytics

**Description:** The Reporting and Analytics module provides users (especially program managers, finance managers, and executives) with insights into the usage and effectiveness of their rewards and incentive programs. It aggregates data collected by the system (rewards sent, redemption rates, spending by category, etc.) and presents it in an understandable format, including charts, summary statistics, and detailed breakdowns. The goal is to help stakeholders measure ROI, identify trends, and make data-driven decisions (such as adjusting reward types or targeting areas of low redemption).

The system will include a set of standard reports and possibly allow some customization or filtering. These reports might overlap somewhat with tracking and budgeting, but are more about summarizing and analyzing over time or by category, rather than operational tracking of individual items.

**Functional Requirements:**

- **FR 3.8.1 Dashboard Metrics:** The platform’s main Dashboard (for authorized users) shall display key high-level metrics in a concise way. For example:
  - Total Rewards Sent (this month/quarter or all-time, perhaps compared to previous period).
  - Total Spend on Rewards (in the period, vs budget).
  - Overall Redemption Rate (percentage of sent rewards that have been redeemed).
  - These metrics provide a quick health check of programs.
  - Org Admins might see company-wide numbers, while a Program Manager might see metrics for programs they manage only (depending on scope and filters).
- **FR 3.8.2 Standard Reports:** The system shall provide several pre-defined reports, accessible from a Reports section. Examples:
  - **Redemption Rate Report:** Shows number of rewards sent vs redeemed, broken down by campaign, by reward type, by month, etc. e.g., a chart of redemption percentage per campaign.
  - **Spend by Category Report:** How spending is distributed across reward categories or departments. e.g., $X on digital gift cards, $Y on physical gifts; or $A by Marketing team, $B by Sales team.
  - **Budget Utilization Report:** For each budget, how much is used vs allocated over time (could be a table or bar chart).
  - **Top Rewards Report:** List the most frequently chosen rewards or most expensive rewards given. e.g., “Amazon $50 - 120 times, Starbucks $10 - 200 times, Company Mug - 50 times, etc.” This indicates popularity.
  - **User/Participant Report:** Perhaps identify if certain recipients have gotten multiple rewards (if that’s relevant, could be useful to see if one customer got 5 rewards from various campaigns).
  - If research, possibly a report on average incentive per response, etc.
  - We identify likely ones: redemption rates, spend vs budget, breakdown by type, timeline of usage.
- **FR 3.8.3 Filtering and Drill-down:** Users should be able to filter report data by relevant dimensions:
  - Time period (date range selection).
  - Specific campaign or program.
  - Department or budget.
  - Reward type or category.
  - For example, the Finance Manager may filter the Spend report to just Q4 2024 and just marketing department budget.
  - The UI should update the charts/tables accordingly.
  - Drill-down: e.g., clicking on a segment of a chart (like the bar for a particular campaign) could drill to a more detailed view of that campaign’s data (or take the user to the list of rewards in that campaign in the tracking section). This integration between reports and underlying data is useful.
- **FR 3.8.4 Data Visualization:** Reports shall include clear data visualizations:
  - Use charts (bar, line, pie) where appropriate:
    - Trend over time (line chart of rewards sent per month).
    - Breakdown (pie chart of spend by category or bar chart of redemption rate by campaign).
  - Use tables for detailed figures (like a table of campaigns with sent/redeemed counts, or a table of top recipients, etc.).
  - Include totals and subtotals where helpful.
  - Ensure charts have legends, axes labels, and are color-blind friendly in design (part of UX).
- **FR 3.8.5 Report Exporting:** Users (with appropriate permission) shall be able to export report data:
  - Perhaps export as CSV for the underlying data of a report (e.g., a CSV of all campaign stats).
  - Possibly PDF export of a nicely formatted report view (with charts). This could be useful to drop into presentations. If PDF is complex, at least allow printing the page cleanly.
  - Export options might include: CSV, Excel, PDF.
- **FR 3.8.6 Custom Reports (Future/Advanced):** Possibly allow users to create a custom query/report:
  - e.g., “I want a report of all rewards of value > $100 and whether redeemed, in last year”.
  - This could be done via a UI or by exporting data and using external tools. Initially, we may stick to fixed reports and provide enough filters.
  - If needed, an admin could pull a full data export of all reward transactions and pivot as they please offline.
- **FR 3.8.7 Performance of Reporting:** If data volume is large, generating reports might take time.
  - The system could pre-compute some aggregates (like daily totals) to speed up queries, or use a separate analytics DB or data warehouse if needed.
  - But within the SRS: the requirement is that report pages should load within a reasonable time (e.g., a few seconds for moderately sized data).
  - For extremely large queries, consider asynchronous generation with a “Your report is being prepared” message, though prefer real-time for typical use.
- **FR 3.8.8 Permissions for Reports:** Ensure that users only see data they are allowed to:
  - Org Admin and Finance likely see all data.
  - A Program Manager might see only their campaigns or those for which they have access. If a manager should see only their department, implement tagging of campaigns by department and filter accordingly.
  - A Viewer might have access only to a specific summary report but not detailed breakdowns.
  - These access rules should be consistent with RBAC definitions.
- **FR 3.8.9 ROI and Effectiveness Indicators:** The platform might include or allow input of outcome data to correlate with rewards:
  - For instance, if known, the system could show “We sent 100 referral rewards and gained 80 new customers” if integrated with their referral system. That’s beyond our scope to know.
  - More realistically, we provide the data about the rewards; the user can manually evaluate ROI by comparing with other business data.
  - However, an optional feature: allow attaching an “outcome metric” to a campaign to track ROI (like revenue generated, etc.). This might be manual entry by the user or an API integration. Probably too advanced for now.
- **FR 3.8.10 Trends and Insights:** The system might highlight notable insights:
  - E.g., “Redemption rate increased 10% this quarter compared to last”.
  - Or “Physical gifts have significantly lower redemption (40%) than e-gifts (90%)” – which might be gleaned from data.
  - This is more on the analytics/insights side and could be a future addition with machine analysis, not required initially beyond the data presentation.
- **FR 3.8.11 Multi-Org Reporting (Platform):** Not for end users, but for the platform provider, maybe an overall usage report of all clients (for our internal monitoring or billing if needed). This is separate from client-facing reports.

In summary, the reporting features turn the raw data collected by the platform into actionable information. Product Managers can see if their incentive program is performing (are people using the rewards?), Finance can see where the money is going and that it aligns with plans, and everyone can better understand the impact of their reward strategies.

## 4. UI/UX Requirements

_(Note: Many UI/UX expectations have been interwoven in previous sections. This section highlights overarching UI/UX principles and any additional requirements specifically about user interface design and user experience that haven’t been covered.)_

### 4.1 General Usability and Design Principles

- **Consistency:** The application’s look and feel should be consistent across all modules. Use a unified color scheme (with the ability to incorporate the client’s branding in certain areas), and consistent UI components (buttons, tables, form fields) to reduce the learning curve. For example, all primary action buttons might be a specific color, icons used for similar actions (like edit, delete) should be identical in different pages.

- **Responsiveness:** The UI shall be responsive and render properly on various devices and screen sizes. While the primary users (admins/managers) will likely use desktops, recipients will often use mobile for redemption. Hence:

  - The admin interface should be usable on at least tablet-sized screens and potentially smaller in a pinch.
  - The redemption pages absolutely must be mobile-friendly.
  - Use responsive design frameworks (CSS grid/flexbox, etc.) to adjust layout.

- **Clarity and Simplicity:** Interfaces should be clean and not overly cluttered. Use whitespace and grouping to make it easy to scan information. For example, on the reward send form, group recipient info, reward selection, message in sections. In reports, highlight key numbers in large font.

  - Text should be concise and jargon-free (use terms the business users understand, e.g., "Send Reward" instead of "Initiate Reward Delivery Process").
  - Provide helpful hints or tooltips for anything not obvious. E.g., a tooltip on “Budget” field saying “Select which budget this will count against”.

- **Navigation:** Provide a clear navigation menu or sidebar for major sections: Dashboard, Rewards/Campaigns, Catalog, Budgets, Reports, Admin (depending on role). The current section should be highlighted. Use bread-crumbs on deeper pages if necessary (e.g., when viewing a specific campaign, show "Campaigns > Q1 Referral Campaign").

- **Feedback and Confirmation:** As noted earlier:

  - When a user performs an action (send, save, delete), show immediate feedback: a success message or error alert.
  - If an action is irreversible or significant (like deleting a user or canceling a reward), ask for confirmation (“Are you sure? This cannot be undone.”).
  - Use modal dialogs or confirmation pop-ups appropriately.

- **Error Handling:** Error messages should be user-friendly and indicate what went wrong and how to fix it. E.g., “Email address is invalid, please check the format” rather than just “Error in field email”.

  - If a server error occurs, show a generic apology and maybe a reference code, but avoid exposing technical details.
  - Validation errors should be displayed near the relevant field and/or as a summary at top.

- **Performance:** UI interactions (like opening a page) should generally occur quickly. If a page is loading data and might take more than a second, show a loading spinner or progress bar so the user knows the system is working.

  - Avoid blocking UI without feedback.

- **Accessibility:** The UI should strive to meet accessibility guidelines (WCAG 2.1 AA):

  - Ensure all interactive elements are reachable via keyboard (tab order logical, press Enter to activate a button, etc.).
  - Provide text alternatives for icons/images (e.g., alt text or aria-label on icon buttons).
  - Ensure color contrasts are sufficient for readability.
  - This is particularly important for any user-facing pages (the redemption page definitely, admin interface as well because companies may have employees with disabilities managing programs).

- **Internationalization:** If multiple languages are supported (see Localization requirements in section 3.10), the UI must be designed to accommodate text expansion (some languages take more space) and possibly right-to-left layouts. Ensure UI strings can be replaced with translations easily and that date formats, etc., adjust.

- **Branding and White-Label:** The platform should allow some branding customization per client:
  - Upload a company logo to display on the dashboard and in emails/pages that recipients see.
  - Possibly choose a primary color to use for accents to feel on-brand.
  - The overall layout likely remains the same (as it’s our SaaS product UI), but these touches integrate the client’s identity.
  - White-label in emails: use the sending company’s name in sender line and possibly their domain for sending email if configured (via SPF/DKIM setup). So recipients see it as from that company.
  - This improves trust in the communications.

### 4.2 Key User Interfaces

To ensure clarity, here are outlines of key screens:

- **Login Page:** Simple login form (email + password) or buttons for SSO providers. Company logo or name if known (some multi-tenant apps have you enter email first, then show company branding if domain is recognized).
- **Dashboard:** Summarize important info with tiles or cards (e.g., “Rewards sent this month: 120”, “Redemption Rate: 85%”, “Active budgets: 3”). Possibly a graph of rewards sent over last 6 months. Show any pending tasks (like “2 approvals awaiting your action”).
- **Reward Send Form:** A page or modal where user selects reward, enters recipients (with maybe an auto-complete if we store contacts, or a text area or file upload), composes message, chooses send now or schedule, and selects budget. It should present these in a logical order top-to-bottom. The “Send” button at bottom triggers confirmation.
- **Bulk Upload Contacts:** If a file upload is part of send flow, after upload show a preview of parsed emails and highlight any errors for correction (maybe in a scrollable area).
- **Campaign/Program Creation (if applicable):** Possibly allow user to create a named campaign with description, select a budget, then later send multiple batches under it. This might be done implicitly just by tagging sends with a campaign name. If explicit UI, it would be similar to scheduling a program with start/end dates and target recipients criteria (though criteria-based automated distribution may be future feature).
- **Reward Tracking List:** Table of rewards (as described in 3.3). Could have filters on top (dropdowns or checkboxes for status).
- **Reward Detail Modal:** If user clicks on a reward in list, open a modal with full details and action buttons (Resend, Cancel).
- **Budgets List:** Show each budget like a card or row: “Marketing Q1: $10,000 total, $8,000 used (80%), $2,000 remaining.” Possibly color the usage (green if far from limit, red if almost exhausted).
- **Budget Detail:** Could show a chart of spend over time and a table of every transaction (reward) logged against it.
- **User Management:** List of users in org with columns (Name, Email, Role, Last login, Status). Buttons to invite new user. Click a user to edit (change role, deactivate). Deactivated ones maybe in a separate list or marked.
- **Reports Interface:** Perhaps each report is a separate page with its own filters and charts. Alternatively, one page with multiple tabs for different reports.
  - E.g., a tab for “Overview” showing high-level charts, another for “By Campaign”, “By Reward Type”, etc. Depending on amount of content.
- **Settings Pages:** For org admin: include sections for Email Templates (maybe edit the default text that goes out with rewards), SSO setup (upload certificate or metadata), API/Integration keys (generate API keys or set webhook URLs), etc. These are advanced admin settings that not all will use, but should be organized logically.

### 4.3 Visual Design and Layout

- Use the company’s branding for platform design but allow injection of client branding in specified places. Possibly a neutral design (blues/greys) that doesn’t clash with adding a client logo.
- Ensure visual hierarchy: important numbers or headings should be more prominent. e.g., use larger font or bold for totals, use color highlights to draw attention to key statuses (e.g., red text for “Failed” status).
- Icons: use standard icons for edit (pencil), delete (trash), send (paper plane), download (down arrow or similar). This makes the UI intuitive.
- Modal dialogs for tasks like confirming deletion or showing a form in context (like reward detail actions).
- Spacing: avoid cramming too much on one screen; better to use tabs or wizards for multi-step tasks (like a wizard for bulk send if needed).
- Responsive specifics: On small screens, a table might turn into a card list (each record on its own block with labels).
- Provide navigation breadcrumbs or back buttons to ease moving around (e.g., from a report detail back to main reports).

### 4.4 Internationalization and Localization UX

_(If multi-language support is planned)_:

- Provide a language switcher (perhaps in user profile or a dropdown in footer).
- Ensure UI strings come from resource files so they can be translated easily.
- Dynamic content like date/time and numbers format according to locale (e.g., using libraries to display “12/31/2025” vs “31.12.2025”).
- Double-check text expansion: e.g., a button that says “Send” in English might be “Envoyer” in French (longer) – design button width to accommodate likely expansion (~30%).
- If supporting RTL languages, ensure the layout flips appropriately (this might require using a CSS framework or adding a body class that changes direction).
- The redemption emails should also be localized if needed (e.g., send Spanish text to Spanish recipients, which implies tagging a preferred language per recipient or per campaign if known).

### 4.5 Recipient UX Specifics

As recipients are external, their UX is primarily the email and redemption page:

- The email should be visually appealing, likely with some graphical element (like the company logo or a gift icon). Not just plain text unless needed for deliverability; an HTML email template is ideal.
- The redemption page should be lightweight (it might be accessed by many people), quick to load, and possibly branded with the company's theme (maybe use their logo and a banner image).
- If a recipient encounters a problem, the support info given should route them to someone in the sending company or our support as appropriate. Possibly provide a unique code or reference in the email for support to quickly look up the reward (like “Reward ID: 12345”).
- After redemption, maybe prompt any next steps (e.g., “Enjoy your reward! If you have issues using the code, contact [Gift Card provider] or [Company].”).

### 4.6 Onboarding and Help

- When a new Org Admin first logs in (especially during trial or initial setup), the system could provide a quick onboarding wizard or tips:
  - E.g., “Welcome! Start by adding your team and configuring your catalog preferences.”
  - Maybe highlight where to go to invite users, create budgets, etc.
- Provide a help center link or documentation accessible from within the app (could be a link to an online help page).
- Possibly context-sensitive help: small “?” icons next to complex settings linking to a help article.
- Tooltips on hover for icons or truncated text.

### 4.7 Performance and Scalability in UX

- The UI should handle reasonably large data sets gracefully:
  - If an org has thousands of rewards, the tracking list should use pagination or virtual scrolling.
  - Not freeze browser by trying to render 10k DOM rows at once.
  - Same for user lists, etc., though those will be smaller typically.
- Provide search in tables to quickly find items rather than scrolling page by page.

### 4.8 Browser Compatibility

- Support latest versions of Chrome, Firefox, Safari, Edge (which covers most users).
- Basic functionality should work in Microsoft Edge (Chromium-based) which covers IE replacement; we likely drop Internet Explorer 11 support (it’s deprecated).
- Ensure no dependency on technologies not supported by these (like avoid old IE issues, use polyfills if needed for any new JS features).

In conclusion, the UI/UX requirements aim to make the IncentiveHub platform intuitive, efficient, and pleasant to use for all user roles, while also providing a smooth experience to reward recipients, who are an indirect but important audience of the system.

## 5. Non-Functional Requirements

This section outlines requirements that describe how the system performs and operates, rather than specific features. These include performance, security, maintainability, scalability, reliability, and compliance considerations. While they may not be directly visible to end users, they are crucial to ensure the platform meets enterprise standards and runs smoothly under expected conditions.

### 5.1 Performance and Scalability

- **NFR 5.1.1 System Throughput:** The platform shall be capable of handling a reasonably high volume of transactions for a mid-sized enterprise:
  - Support at least **hundreds of concurrent users** (admins/managers across all tenants combined).
  - Be able to process on the order of **10,000 reward sends per hour** during peak load across all customers without significant slowdown (this includes generating reward codes, sending emails, updating statuses).
  - The design should allow scaling beyond this (see scalability below) for larger clients.
- **NFR 5.1.2 Response Times:**
  - The web application (for admin users) should have **page load times** of under 3 seconds for typical pages (dashboard, lists) when used under normal load.
  - Key user actions like submitting a reward send should process within 2-3 seconds before providing feedback (not counting background email delivery which can happen asynchronously). Essentially, the user shouldn’t wait long to see a confirmation.
  - The redemption page for recipients should load within 2 seconds on a standard connection, and showing a code after clicking should be near-instant (<1 second).
  - Reports queries might involve more data; they should still aim to display within 5 seconds for moderately large data sets (say a year’s data for 5,000 rewards). If more, consider asynchronous generation.
- **NFR 5.1.3 Scalability:** The system architecture shall be scalable such that:
  - Additional application server instances can be added to handle more concurrent users or transactions without major rework (horizontal scaling).
  - The database should be able to scale (vertical scaling to a point, with ability to introduce read replicas for heavy read/report load).
  - Critical background processing (like sending emails for bulk rewards) shall be handled by a queuing system that can scale workers up to meet demand spikes.
  - The design should separate concerns (web frontend, application logic, background jobs, database) so they can be scaled independently as needed.
- **NFR 5.1.4 Bulk Operations Performance:** For large bulk reward distributions (e.g., sending 5,000 rewards in one go):
  - The system will queue and send these in batches so as not to overwhelm memory or external services. Users will get timely feedback and completion notifications, but the system might be processing in background for several minutes.
  - This should not block other operations; others can use the system normally while a bulk job runs.
- **NFR 5.1.5 Data Volume:** The system shall be designed to handle growth of data:
  - On the order of at least **1 million reward records** in the database without performance degradation in tracking and reporting (this might happen over years of usage for big companies).
  - Use proper indexing on common query fields (date, status, campaign, email) to maintain query speed.
  - Archival strategies might be planned if data grows beyond that (like archiving older than X years), but aim to avoid that necessity within reasonable horizon.
- **NFR 5.1.6 Content Delivery:** Use of CDNs for static assets (images, CSS, JS) to improve load speed globally.
  - For recipient-facing content like images on redemption pages or email images, definitely use CDN to speed up delivery to various regions.
- **NFR 5.1.7 Efficiency:** The application should be reasonably efficient in resource usage to keep hosting costs manageable.
  - Use connection pooling for DB, don’t hog CPU on tight loops, etc. This is more internal design guidelines.
  - But it can also reflect in cost to the client if usage is heavy (especially if we have cost models, but that’s business, not need to detail).
- **NFR 5.1.8 Graceful Degradation:** In extreme load scenarios, the system should degrade gracefully rather than fail completely:
  - E.g., if reporting queries are too slow under heavy load, maybe queue them or show partial data rather than crashing.
  - If the email service slows, the queue will back up but UI should still accept requests and show them as pending rather than timing out user actions.

### 5.2 Security Requirements

- **NFR 5.2.1 Authentication Security:**
  - All communication involving authentication credentials shall be done over HTTPS (no plaintext credentials over the network).
  - Passwords stored in the database must be hashed with a strong algorithm (e.g., bcrypt or Argon2) with proper salting.
  - Implement account lockout or CAPTCHA after a certain number of consecutive failed login attempts to deter brute force attacks.
  - If using JWT or session tokens, ensure they are signed and have short expiration with refresh logic to reduce risk.
  - Support multi-factor authentication (MFA) for users, at least for Org Admins, either via an authenticator app or SMS/Email OTP (this could be optional, but being SOC 2 compliant often encourages MFA for admin accounts).
- **NFR 5.2.2 Authorization Controls:** The system’s RBAC (as defined in 3.6) must be strictly enforced on the server side for all actions:
  - Every API endpoint or server function should verify the user’s role and permissions.
  - This ensures even if someone manipulates the client or finds an unintentional way, they cannot perform actions beyond their role’s privileges.
  - For example, a Finance Manager’s session token should not be able to invoke a “create user” action (server will check role and reject).
- **NFR 5.2.3 Data Encryption and Protection:**
  - All sensitive data at rest shall be encrypted at the storage level (e.g., database encryption or disk encryption) as a precaution (especially required if storing PII like names, emails – which we do, and any reward codes possibly considered sensitive).
  - Particularly, reward codes for high-value items might be considered sensitive; we might store them encrypted in the DB, and only decrypt on display to the user at redemption time.
  - Ensure backups are also encrypted.
- **NFR 5.2.4 Network Security:**
  - The system shall be deployed in a secure network environment with necessary firewalls. Only required ports (e.g., 443 for HTTPS) are open to public; internal databases not accessible publicly.
  - Use TLS 1.2+ for all external communications. Keep certificates updated and use strong cipher suites.
  - If multi-tenant data in one database, enforce tenant isolation with proper queries (e.g., always filter by org_id in queries; possibly use SQL row-level security or separate schemas if high security needed).
- **NFR 5.2.5 Vulnerability Management:**
  - Develop the system following secure coding best practices to avoid OWASP Top 10 vulnerabilities (SQL injection, XSS, CSRF, etc.).
  - For instance, use parameterized SQL queries or an ORM to prevent injection.
  - Implement CSRF protection on state-changing POST requests (e.g., an anti-CSRF token or rely on same-site cookies if that approach).
  - Use output encoding on any data displayed in the UI to prevent XSS (particularly if any custom message content might have HTML, though we might strip or not allow HTML in user inputs).
  - Regularly update components and libraries to fix security issues.
  - Penetration testing and vulnerability scanning should be conducted periodically (not a feature of the product itself, but a requirement in deployment).
- **NFR 5.2.6 Audit and Monitoring (Security):**
  - As detailed in 3.7, maintain audit logs of security-relevant events (logins, role changes, etc.) and ensure they are monitored.
  - Possibly integrate with a SIEM (Security Info and Event Management) system for alerting on suspicious activity (like multiple failed logins or unusual times).
  - This is more operational but may be required for compliance (SOC 2 etc.).
- **NFR 5.2.7 Privacy and Data Protection:**
  - The system shall comply with GDPR/CCPA principles: only collect necessary personal data (we mainly have names, emails, maybe phone for SMS).
  - Provide means to delete or anonymize a person’s data if requested (e.g., if a recipient requests deletion, their email might need to be removed or hashed in records after fulfilling legal obligation).
  - Ensure that personal data of recipients is only accessible to the relevant client org and not to others. (Tenant isolation addresses that).
- **NFR 5.2.8 Third-Party Integration Security:**
  - When integrating with external providers (gift card API, email API, etc.), secure the API keys and secrets. Store them encrypted and do not expose in client-side code.
  - Rotate these keys if needed and have a process to update them (through admin interface config).
  - Validate data coming from webhooks or provider callbacks (e.g., use shared secret to ensure a webhook really came from the gift card provider, not an attacker).
- **NFR 5.2.9 Platform Super-Admin Access:**
  - Limit who in our company can access customer data. Access by platform admins to a client’s account (for support) should require secure procedures (like a special login, MFA, and be logged).
  - Perhaps have separate admin portal.
- **NFR 5.2.10 Session Management:**
  - User sessions should expire after a period of inactivity (e.g., auto-logout after 15 or 30 minutes idle, configurable).
  - Provide a remember-me option if needed but still with a relatively short absolute expiry (maybe 30 days max for a token).
  - Invalidate all sessions upon password change or explicit logout.
  - Only one concurrent session per user optional (for higher security, maybe not necessary).

### 5.3 Compliance and Regulatory

- **NFR 5.3.1 GDPR Compliance:** The system shall facilitate compliance with EU GDPR:
  - Maintain a data processing record (internally, not necessarily a feature).
  - For any stored personal data, allow retrieval and deletion:
    - If an EU individual requests a copy of their data, the client’s Org Admin should be able to export what info on that person exists (e.g., search logs, see they got X rewards).
    - If deletion is requested, an Org Admin can delete or anonymize that person’s data (e.g., remove their email from records and replace with a generic identifier in audit logs if needed).
  - Provide consent mechanisms as needed: for example, if sending reward emails to customers, ensure that the business has collected consent or it's part of a transaction (our platform may require them to confirm they've lawful basis).
  - Our system emails should include an option to opt out of future reward emails (as covered in 3.4.12).
- **NFR 5.3.2 CCPA Compliance:** Similar to GDPR, ensure California residents’ rights:
  - Ability to disclose what personal info we have on them (likely just name/email and reward details).
  - Ability to delete if requested.
  - We do not “sell” personal data; we use it only to send the reward.
  - Possibly include “Do not sell” information in privacy policy (though not directly applicable as we aren’t selling data).
- **NFR 5.3.3 SOC 2 Compliance:** The platform will be designed and operated to meet SOC 2 Type II requirements in Security, Availability, and Confidentiality (maybe also Processing Integrity and Privacy):
  - Many security controls outlined (audit logging, access control, etc.) contribute to this.
  - Availability: we will have backups, disaster recovery plans (see reliability).
  - Confidentiality: agreements and technical measures in place to safeguard data.
  - Processing Integrity: ensure that reward transactions are complete, accurate, timely (which our tracking and processes ensure).
  - Privacy: align with privacy commitments (we should have a privacy notice).
- **NFR 5.3.4 Data Residency:** If clients have requirements that data stays in certain regions (e.g., European customer data in EU data center):
  - The platform should be deployable in multiple regions or choose a hosting region that covers majority needs.
  - Possibly offer an EU-hosted instance for EU clients to address data residency.
  - Not strictly a functional requirement for all, but for compliance we may promise where data is stored. So design with flexibility to deploy in different locales if needed.
- **NFR 5.3.5 Email Compliance (CAN-SPAM, CASL):**
  - All email communications must include proper identification of the sender and a way to opt out (even if transactional, it's good practice).
  - Maintain a suppression list for recipients who opted out to ensure we honor not emailing them again (as described in FR 3.4.12).
  - This ensures compliance with anti-spam laws and good deliverability.
- **NFR 5.3.6 PCI Compliance (if applicable):**
  - We are not processing credit cards directly unless we allow purchasing rewards through the platform. If, in future, clients pay through us or we handle gift card payments, we might touch credit card data.
  - For now, likely out-of-scope; the platform deals with prepaid codes and invoices clients outside system. So PCI not triggered, but if it were, would require significant measures (segmented environment, etc.).
  - We'll note: do not store any payment card details on our system unless absolutely needed and then follow PCI DSS.
- **NFR 5.3.7 HIPAA (unlikely applicable):**
  - If the platform were used to reward patients in healthcare research, there's a chance health info is involved. We should avoid storing any health data – only contact info. So likely not a HIPAA scenario.
  - If it ever is, we’d sign BAAs and treat that data with required safeguards (encryption, limited access).
- **NFR 5.3.8 Audit and Documentation for Compliance:**
  - Maintain documentation (security policy, how data flows, etc.) so we can demonstrate compliance to auditors.
  - Not a feature, but a requirement to operate in compliance.
  - Possibly provide to Org Admins upon request some of this info (some companies ask for our SOC 2 report or pen test results).

### 5.4 Availability and Reliability

- **NFR 5.4.1 Uptime SLA:** The system shall be designed for high availability. Target **99.9% uptime** or better for the production service, excluding scheduled maintenance.
  - This means less than ~8 hours of downtime per year.
  - Architect with redundancy (multiple servers, failover DB, etc.) to avoid single points of failure.
- **NFR 5.4.2 Redundancy and Failover:**
  - Deploy at least in a redundant fashion within a region (e.g., multi-AZ on AWS for servers and database).
  - If an app server goes down, others handle load; if primary DB goes down, a standby takes over (with minimal downtime).
  - Load balancers should detect unhealthy instances and reroute traffic.
- **NFR 5.4.3 Disaster Recovery:**
  - Implement daily (or frequent) backups of critical data (database, etc.) and secure them off-site or in a different region.
  - Have a documented DR plan: e.g., ability to restore the service in a secondary region in case of primary region outage (if required by some clients, though might not promise this from start if not needed).
  - RPO (Recovery Point Objective): e.g., maximum data loss of 1 hour (if hourly backups or continuous replication).
  - RTO (Recovery Time Objective): e.g., can bring system back within 4 hours of a major outage.
  - These might not be fully implemented initially, but plan for them as we scale to enterprise expectations.
- **NFR 5.4.4 Maintenance and Updates:**
  - Schedule maintenance windows for upgrades (with prior notification to Org Admins) or attempt zero-downtime deployment techniques.
  - If downtime is needed, do it in off-peak hours and keep it as short as possible.
  - The system should display a friendly maintenance page if accessed during a scheduled downtime.
- **NFR 5.4.5 Monitoring and Alerts:**
  - The system shall be actively monitored (not exactly user facing, but needed to ensure reliability).
  - If any critical service goes down or response times spike, ops team is alerted (via email/SMS).
  - Also monitor specific metrics like email sending success rate; if emails start failing (e.g., provider outage), alert and possibly auto-switchover to backup provider if configured.
- **NFR 5.4.6 Graceful Error Handling:**
  - If a component fails (e.g., gift card provider API is down), the system should handle it gracefully: queue requests, show a message to admins in the platform if known (“Gift card service is currently experiencing issues, sending might be delayed”), and retry later rather than crash or lose requests.
- **NFR 5.4.7 Data Integrity:**
  - Ensure that either a reward is fully recorded and processed, or not at all (transactional integrity).
  - E.g., avoid a scenario where budget was deducted but reward send not recorded or vice versa; use transactions in DB to keep those in sync.
  - If a part fails, roll back or mark clearly for admin to reconcile.
- **NFR 5.4.8 Scalability of Infrastructure:**
  - Use cloud auto-scaling rules if possible to automatically add more capacity under high load and scale down when load decreases, thus supporting reliability under unexpected spikes.
- **NFR 5.4.9 Capacity Planning:**
  - The system should be load tested for anticipated peak usage and have headroom. Regularly re-evaluate capacity as more tenants join.
  - If nearing resource limits (CPU, memory, DB connections), plan upgrades ahead of time to avoid incidents.

### 5.5 Maintainability and Extensibility

- **NFR 5.5.1 Modular Architecture:**
  - The system’s codebase should be organized into modules corresponding to features (e.g., user management, reward handling, budget management, etc.). This separation makes it easier to update or replace components without affecting others.
  - This also helps multiple developers work without stepping on each other.
- **NFR 5.5.2 Code Quality:**
  - Adhere to coding standards and best practices so that the code is readable and maintainable (naming conventions, proper comments for complex logic, etc.).
  - Use version control (obviously) and code reviews to ensure quality and consistency.
  - Ensure adequate unit/integration tests so changes can be verified not to break existing functionality (i.e., maintain a test suite).
- **NFR 5.5.3 Documentation:**
  - Maintain up-to-date documentation for the system’s design and APIs.
  - API documentation (for integration) should be clear for external developers (could be through an online portal or OpenAPI spec).
  - Internal documentation for configurations, deployment, etc., for our devops.
  - This is necessary so new team members or external integrators can understand the system quickly.
- **NFR 5.5.4 Configurability:**
  - Use configuration files or database-stored settings for things that might vary by deployment or tenant, rather than hard-coding (e.g., email server settings, default reward terms, etc.).
  - This makes maintenance easier because changes can be made via config rather than code changes.
  - Also, allow toggling certain features per organization if needed (feature flags) so we can pilot new features with one client without affecting all.
- **NFR 5.5.5 Extensibility:**
  - The design should allow adding new reward provider integrations with minimal impact (e.g., if we add a new gift card vendor, we implement its adapter and plug it in).
  - Adding new report types or new roles in future should be feasible by extending existing structures (like role-permission mapping).
  - Possibly foresee multi-language support even if not immediate, and design text externalization accordingly.
  - Also, ability to support additional channels (like if in future we add WhatsApp or other messaging for delivery) by having an extensible notification service.
- **NFR 5.5.6 Logging and Debugging:**
  - Apart from audit logs, maintain application logs (at various levels: info, warning, error) to help troubleshoot issues.
  - These logs should have enough context (e.g., include request IDs or user IDs when logging an error in processing a request).
  - Ensure no sensitive data is dumped in logs.
  - Make logs easily accessible to developers (via a centralized log management).
  - Good logging and error messages in code make maintaining easier because issues can be pinpointed.
- **NFR 5.5.7 Issue Tracking:**
  - When bugs or incidents occur, maintain an issue tracking system. (Though process, not product feature.)
  - However, could consider an in-app feedback mechanism for Org Admins to report an issue which goes to our support team.
- **NFR 5.5.8 API Versioning:**
  - If and when the public API is updated (backwards-incompatible changes), support versioning (like /v1/ and /v2/ endpoints) to not break existing integrations. Document deprecation timelines.
  - This makes extending the API safer and maintenance of old vs new easier.
- **NFR 5.5.9 Third-Party Components:**
  - Use widely supported third-party libraries and keep track of updates for them.
  - If a library becomes unsupported, plan to replace it to avoid technical debt.
  - This ensures long-term maintainability (avoid being stuck on an outdated dependency).
- **NFR 5.5.10 DevOps and CI/CD:**
  - Employ continuous integration and deployment so that maintenance releases (bug fixes, minor improvements) can be rolled out frequently and reliably with minimal downtime.
  - This implies tests run on each build, etc. Not directly user-facing, but ensures we can maintain quality while making changes.

### 5.6 Privacy and Data Protection (some overlap with compliance)

- **NFR 5.6.1 Data Minimization:**
  - Only store data that is necessary for the operation of the platform. E.g., don’t ask for recipient’s mailing address unless needed for a physical reward.
  - Don’t keep data longer than needed: e.g., allow deletion of expired reward records after a retention period if the client desires (with respect to audit needs).
- **NFR 5.6.2 Data Isolation:**
  - Ensure strict tenant data isolation in the multi-tenant environment, both logically (through code) and if possible at the data level (like row-level security or separate DB schemas).
  - One tenant should never be able to access another’s data via the application. This is absolutely critical for privacy and contractual trust.
- **NFR 5.6.3 Confidentiality Agreements:**
  - All data is considered confidential to the client. We will not use or share their data with third parties except as needed to provide the service (e.g., sending an email via our provider is within providing the service).
  - Internally, employees and contractors must sign appropriate agreements (not part of software, but part of our operations).
- **NFR 5.6.4 Right to Erasure and Right to Access:**
  - Provide means for Org Admin to fulfill a data subject’s request: e.g., search for all data associated with “john.doe@example.com” and export or delete it.
  - This could be partially manual (our support helps the client with a database query) or built-in if we anticipate many such requests. The requirement is that we must comply within legal time frames (GDPR says usually within 30 days).
- **NFR 5.6.5 Anonymization:**
  - If deleting data isn’t feasible because it’s deeply integrated (like removing an email might break referential integrity or audit trails), an alternative is anonymization: replace identifying fields with random or null values while keeping aggregate stats.
  - The system design should consider that possibility (maybe have a method to scrub PII from a reward record while keeping the value and date for stats).
- **NFR 5.6.6 Compliance Audits:**
  - The system and processes will be subject to external audits for compliance (like SOC 2 audit, GDPR compliance checks). We must maintain evidence (like audit logs, policies, etc.) and potentially make changes as recommended by auditors.
  - The development team should be prepared to make minor adjustments to meet compliance (like adding an extra security control) as those audits require.

### 5.7 Operational Requirements

_(Some of these cross into DevOps rather than the software itself, but we note them to cover overall system expectations.)_

- **NFR 5.7.1 Deployment Flexibility:**
  - The software should be deployable on common cloud infrastructure. Ideally containerized (Docker/K8s) to ease scalability and portability. This is not a user feature but influences how we design configs, statelessness etc.
- **NFR 5.7.2 Monitoring and Logs Retention:**
  - Keep application logs at least X days in an accessible form for debugging. Possibly archive older logs to cold storage for Y months for compliance.
- **NFR 5.7.3 Supportability:**
  - Provide admin tools or queries for support staff to easily lookup an organization, user, reward, etc., when a support ticket comes in. (Maybe an internal admin console separate from client UI that allows searching across tenants).
  - This isn’t client-facing, but crucial for maintenance of service.
- **NFR 5.7.4 Environmental Separation:**
  - Have separate environments for dev, test, and production to ensure testing does not affect real data.
  - Possibly a staging environment where clients can test integration (maybe not initially exposed to clients, but at least for our QA).
- **NFR 5.7.5 Legal and Contracts:**
  - The product must adhere to any contractual obligations we have (like SLAs mentioned, or data handling agreements).
  - For example, if a contract promises that data will be stored in EU only, ensure we deploy accordingly or do not accept such a contract unless we can fulfill it.

---

By adhering to these non-functional requirements, the IncentiveHub platform will not only deliver the needed features but will do so in a manner that is performant, secure, reliable, and trustworthy, which is essential for adoption in a corporate environment.

## 6. System Architecture Overview

This section provides a high-level overview of the system’s architecture, describing how the major components of the IncentiveHub platform interact. It outlines the logical tiers of the application, key external integrations, and data flow. This overview is intended to ensure a shared understanding of how different parts of the system come together to fulfill the requirements.

([image]()) _Figure 6.1: High-Level System Architecture._ The architecture consists of a multi-tier application with separation of concerns. Users access the platform via a Web Browser (client), communicating over HTTPS with the **Web Application Server** (which serves the web UI and exposes a RESTful API). The application server handles business logic and interacts with a **Database** for storing persistent data (users, rewards, budgets, logs). A separate **Background Job Queue** and worker processes handle asynchronous tasks like sending emails or processing bulk sends, ensuring responsiveness. The system integrates with several external services: an **Email/SMS Service** for delivering notifications to recipients, one or more **Reward Provider APIs** (e.g., gift card services) for fulfilling rewards, and optionally an **SSO Identity Provider** for user authentication. All components are hosted in a cloud environment with security measures (firewalls, load balancers) and can scale horizontally. Audit logs and monitoring feeds are stored in a secure log repository (not shown) for compliance and debugging.

### 6.1 Application Layers and Components

- **Presentation Layer (Client):** This is the front-end interface accessed via web browser. It could be a single-page application (SPA) built with a framework (React/Angular/Vue) or a server-rendered HTML interface (depending on implementation). Its role is to present data and capture user input for the various functionalities (sending rewards, creating budgets, etc.). It communicates with the server primarily via HTTP(S) requests to the API endpoints, and also renders real-time feedback to users. For recipients, the presentation layer includes the emails and redemption web pages, which are simplified views served often without requiring login.

- **Web/Application Server:** The core of the platform resides on the server side, which includes:

  - **Web Server / API:** Accepts HTTP requests from browsers or integrated systems. It serves static content (if any) and routes API calls to appropriate handlers.
  - **Application Logic:** This is structured into modules or services:
    - _User Service:_ handles user authentication (possibly delegating to SSO for some), session management, user CRUD, and role checks.
    - _Reward Service:_ handles the creation of reward records, coordination with external providers to generate codes or orders, and initiation of notifications. It also triggers updates to status and logs events.
    - _Notification Service:_ a sub-component responsible for interfacing with email/SMS gateways. For example, it formats the email content (merging in personalization and links) and calls the Email API to send. For SMS, similarly uses SMS API.
    - _Budget Service:_ enforces budget rules, updates remaining balances when rewards are sent or redeemed, triggers approval workflow if needed.
    - _Audit Log Service:_ an aspect that logs each event to the audit store.
    - _Reporting Service:_ handles the aggregate queries for reports. It might access a read replica or perform calculations (or in some designs, maintain pre-aggregated data for quick retrieval).
    - _Integration Service:_ deals with external APIs (gift card providers, perhaps Slack or CRM if integrated). Could be separate modules for each integration to keep code modular.
  - This server could be built with a framework (Django, Express, Spring, etc.) with clear separation for controllers (handling web/API requests) and services (business logic), and a data access layer for database interactions.

- **Database:** A relational database (e.g., PostgreSQL or MySQL) will store structured data: user accounts, organization info, rewards (each reward record with all its details and status), budgets, audit logs, and configuration (like integration settings, templates, etc.).

  - We’ll use relational DB for transactional integrity (ensuring budgets and rewards updates occur reliably together).
  - Some data might be in JSON columns if flexible (like storing a blob of audit detail), but mostly structured tables with relationships (each reward row links to an org, possibly a campaign, and a budget; user table links to org, etc.).
  - The DB will enforce unique constraints (like one email per user per org) and maybe foreign key constraints for referential integrity, though in a multi-tenant context we might enforce via application logic instead.
  - The database will be the main source of truth for all records.

- **Background Job/Queue:** For tasks that need to run asynchronously or could be long-running, the architecture includes a job queue (like RabbitMQ, AWS SQS, or a built-in job scheduler in the framework).

  - For example, a bulk send to 1000 recipients: the web server on receiving this request will create a “SendBulkRewards” job with all details and push it to the queue, then immediately respond to the user that it’s scheduled.
  - **Worker processes** (one or multiple, can scale horizontally) consume jobs from this queue and execute them: generating codes by calling provider APIs, sending out emails, updating statuses progressively.
  - Similarly, scheduled sends might be implemented as jobs queued at specified time (or a scheduler that enqueues jobs when time triggers).
  - This decoupling ensures the web interface remains responsive and we can retry jobs on failure without user intervention.

- **Integration Points:**
  - **Email/SMS Gateway:** e.g., SendGrid, Mailgun, or AWS SES for email; Twilio for SMS. The app server or worker calls their API (usually via an SDK or REST call) to send out messages. These services may send back webhook events (like delivered or bounced notifications) to our application. So we will also expose endpoints to receive these and update our records (like marking a reward as undeliverable if bounce webhook comes).
  - **Reward Providers:** e.g., an external Gift Card API such as Tango Card, Blackhawk, etc. Our system communicates with them to either place an order for a gift card code in real-time or retrieve from a pre-purchased pool. This likely happens in the Reward Service logic (synchronously for one-off send, or as part of background job for bulk). We must secure these communications (API keys stored in config). If one provider fails, ideally our architecture could support multiple providers (maybe an abstraction layer).
  - **SSO Identity Providers:** If a client configures SAML or OAuth SSO, the architecture includes either an SSO module or relies on a service. Typically, the web app would redirect to IdP and receive a token/assertion which our server verifies (or we might use a middle library). Post verification, our app either logs the user in (matching email to a user account) or creates one on the fly if allowed. The architecture thus includes trust relationships with external IdPs but doesn't require persistent connection (just during login process).
  - **Others:** Possibly integration with CRMs or other systems via our API or webhooks, but those don't affect our internal architecture except providing API endpoints and maybe processing incoming webhook calls. For example, if a client’s system calls our API to trigger a reward send, it goes through the same App Server logic as a manual send.
- **Security Components:**
  - **Authentication**: likely managed via sessions or JWTs. If sessions, a session store (could be in-memory or a fast database like Redis) might be used, or rely on DB if low volume. With JWT, no store needed but manage keys securely.
  - **Encryption**: ensure TLS at the load balancer for all client-server and server-provider traffic. Database encryption at rest is managed by cloud (e.g., enabling RDS encryption).
  - **Firewalls**: The diagram assumes front-end requests go through a load balancer or reverse proxy which can also serve as WAF. The app server sits in a private subnet, DB in another, accessible only by app servers.
  - **Key Management**: secrets (API keys for email, providers, encryption keys for gift card codes etc.) likely stored in a secure vault or config with limited access.
- **Auditing and Logging:**
  - The application logs events to the audit log table and also normal app logs to a logging system (like files or stdout aggregated by a cloud log service).
  - Those logs should be stored securely (with restricted access).
  - If needed, a separate service or scheduled job might archive or purge old logs per policy.

### 6.2 Multi-Tenancy and Data Isolation

- All data is partitioned by **Organization (Tenant)**. Each relevant table will have an Org identifier. The application will include that filter in all queries (ensuring user’s session carries an Org context).
- Alternatively, separate schema or database per tenant could be used if needed for extreme isolation, but that complicates scaling with many small tenants. Likely we use a single schema and logical isolation.
- Access control on queries ensures one tenant cannot see another's data.
- The architecture allows adding new tenant organizations easily (just a new row in org table, and an admin invites users).
- Configurations that vary by org (like SSO settings, custom catalog toggles) are stored in tables keyed by org.
- This design is flexible to support many orgs on the same infrastructure; if a particular client is huge, we could migrate them to a dedicated instance (the architecture would allow deploying a separate stack just for them if needed – but the codebase is same).

### 6.3 Scalability and Deployment

- The system will likely be deployed in a cloud environment (like AWS). We envision:
  - **Load Balancer:** routes traffic to multiple App Server instances. Also offloads SSL.
  - **App Servers:** stateless (don’t store user session or other data on local disk; use DB or Redis for session if needed) so they can scale horizontally. During a high load (e.g., an entire company sending holiday gifts at once), we can increase number of workers to handle all email sending jobs.
  - **Database:** a primary relational DB for writes and strong consistency. Possibly read replicas for heavy read operations like generating large reports concurrently with writes (to reduce load on primary).
  - **Cache:** We might introduce a caching layer (Redis or similar) for frequently accessed but rarely changed data (like reward catalog data, or configuration) to reduce DB hits and latency.
  - **Queue & Worker:** For background tasks – could be separate processes or container services apart from the web app, but connecting to same DB and using something like Redis or a cloud queue for task distribution.
  - **CDN & Storage:** If storing images (like reward image, or possibly if users upload list files or something), use cloud storage (S3) and deliver via CDN. Emails might embed images hosted on CDN.
- **Auto-scaling:** The system can be set to auto-scale App Servers and workers based on CPU or queue length. This ensures we meet performance under spike.
- **Redundancy:** Duplicate each component (at least two app servers, multi-AZ DB, etc.) so that a single failure doesn’t bring down system.
- **Backup:** The DB is backed up daily or with continuous backup to meet RPO. Those backups are stored durably (e.g., S3).
- **Monitoring:** Tools in place to monitor metrics like CPU, memory, DB connections, queue length, email delivery success, etc. Also monitors external dependencies – e.g., if the gift card API is failing, can alert.
- **Deployment approach:** Likely containerize the app and use something like Kubernetes or ECS. That provides the ability to roll out updates with minimal downtime (rolling updates).
- **Environment isolation:** dev/test vs production using separate clusters or at least separate DB/s.

### 6.4 Extensibility of Architecture

- The architecture is modular, meaning we can plug in:
  - New reward provider integrations by adding new code in the Reward Service that implements a provider interface.
  - Additional notification channels by extending Notification Service to call, say, a WhatsApp API in addition to email/SMS.
  - Additional front-end interfaces (for example, a mobile admin app or a CLI tool) using the same REST API.
  - The presence of a well-defined REST API means external systems (like the client’s CRM or app) can integrate to trigger rewards or fetch status, which is an architectural plus for extensibility.
- If usage grows massively, one could split services further (microservice architecture):
  - e.g., separate the Audit Log service into its own process or the Reporting service into its own service that hits a data warehouse. The current architecture is modular enough to allow extraction if needed.
- The architecture also accounts for compliance: it can be deployed in isolated environments per region if needed (e.g., an EU deployment vs US deployment for data residency).
- Logging and telemetry are central, so we can analyze usage patterns and identify performance issues or errors across the distributed components.

### 6.5 Example Workflows in Architecture (to illustrate interactions)

- **Sending a Reward (Manual via UI):**
  1. Program Manager fills send form on browser, hits “Send”.
  2. Browser calls `POST /api/rewards` with payload (recipients, reward type, message, budget).
  3. Web Server’s Reward Controller authenticates session, authorizes that user can send (checks role, budget access).
  4. Reward Service logic: checks budget availability (calls Budget Service which queries DB and maybe locks budget row), reserves budget amount.
  5. Reward Service calls Provider Integration (e.g., calls gift card API) to get a code. If synchronous and quick (<1s), do it in request; if could take longer, might offload to job.
  6. Assuming quick, it gets code, stores reward record in DB with status “Sent” (and maybe code encrypted).
  7. Calls Notification Service to send email. That might put a job on queue to actually send, or if using an async mail API, might call it directly. Likely put on queue to not make user wait.
  8. Respond to browser with success (perhaps including reward tracking ID).
  9. A background worker picks up the email job, formats the email (pulling reward details from DB), sends via Email API. Email API responds accepted.
  10. If Email API later posts a delivery or bounce webhook, our system’s endpoint (Notification Controller) receives it, finds the reward by some identifier in the webhook payload, then updates status (Delivered or Failed) in DB.
  11. Recipient gets email, clicks link -> redemption handled as previously described (that triggers maybe an update to Redeemed status by hitting our API endpoint when code is shown).
  12. Budget Service later sees reward redeemed (or if we count on send, it was already counted).
- **Bulk Send via Integration (via API):**
  - If an external system triggers, it calls our REST API (with an API key or OAuth token for authentication) to send a reward. The process on server side is the same as above from step 3 onward. The external system would get a response and possibly subscribe to our webhooks for redemption events.
- **Report Generation:**
  - User clicks "Generate Report X". The request goes to Report Controller.
  - If data is moderate, it queries the DB (perhaps a read replica) for aggregated data. Could be done via SQL GROUP BY or via an in-memory process.
  - It returns JSON which front-end uses to render chart via a library (or server could pre-render a chart image, but likely client-side).
  - If data is huge, the controller might immediately respond with “report requested, will email you when ready” and push a job to do heavy aggregation (or uses a cached precomputed result updated daily).
- **Scheduled Reward Execution:**
  - A scheduled send is stored in DB with future send_time. A background scheduler (could be a small cron job or a feature of the queue system) periodically scans for due tasks.
  - When time hits, it creates a job same as if user had triggered now. That job goes through normal send workflow.
- **SSO Login:**
  - User goes to our login, chooses "Login with SAML". We redirect to IdP, user authenticates, IdP sends us a SAML response to our Assertion Consumer Service endpoint.
  - Our Auth Service validates it (using certificate), extract user email and maybe name/role.
  - If user exists in DB, we create session for them. If not, possibly auto-create a user with default role (or deny if we don't auto-provision unless flagged).
  - Then proceed to app normally.

This architecture is robust, scalable, and aligns with the need to integrate external services and support enterprise-grade security and compliance. It separates core concerns, which simplifies maintenance and allows each part to scale or change as needed (for instance, if we switch email provider, only Notification Service code/config changes; if we add a new type of reward provider, only Reward Service integration changes).

## 7. Use Case Scenarios & User Journeys

To validate the requirements and architecture, we describe a few realistic use case scenarios covering the main target uses: employee gifting, partner incentives, customer loyalty, and research incentives. These narratives show how a user would interact with the system and how the system responds, step by step.

### 7.1 Corporate Employee Gifting (Employee Engagement Scenario)

**Objective:** An HR manager wants to reward all employees with a $50 gift card as a holiday bonus.

- **Actors:**
  - HR Manager (Org Admin or Program Manager role),
  - 200 Employees (Recipients).
- **Preconditions:**
  - The HR Manager has a prepared list of all employee emails (perhaps already in the system if integrated with HR).
  - A budget “Employee Rewards 2025” with sufficient funds ($50 \* 200 = $10,000) is set.
  - The $50 gift card (e.g., Visa Prepaid or Amazon) is available in the catalog.
- **Trigger:** HR Manager logs into IncentiveHub in early December to send out the holiday gift.

**Main Flow:**

1. **Initiate Bulk Send:** The HR Manager navigates to “Send Rewards” > “Bulk Send to Multiple Recipients” (if such a menu exists) or on Dashboard clicks a “Holiday Gift Campaign” quick action.
2. **Select Reward:** On the send form, she selects the reward type: "$50 Holiday Gift Card" (a pre-configured choice that might correspond to a Visa card).
3. **Select Recipients:** She uploads a CSV of employees or selects an existing group "All Employees". The system parses 200 emails. It's large, so it shows "200 recipients added."
4. **Compose Message:** She types a message: "Thank you for your hard work this year! Please enjoy this $50 gift card as a token of our appreciation. Happy Holidays!".
5. **Choose Budget:** She picks the "Employee Rewards 2025" budget from a dropdown (if not auto-selected).
6. **Schedule or Send:** She chooses to send immediately (or maybe schedules for Dec 20, either way).
7. **Confirm:** She clicks "Send". The system might pop up "You're about to send 200 rewards costing $10,000 from budget (Remaining after send: $2,000). Confirm?" She confirms.
8. **Processing:** The system validates budget (there is enough, 10k out of maybe 12k available, passes) and begins processing:
   - It generates 200 reward entries in the database (or one entry with 200 recipients, depends how we model, but likely separate entries for tracking each).
   - It enqueues 200 email sending jobs (or batches of e.g. 50 per job, to manage load).
   - It immediately shows HR Manager a success message: "200 rewards are being sent. You can track progress in the Rewards page."
9. **Email Delivery:** Over the next couple of minutes, the background workers pick up those jobs:
   - For each, call gift card API to fetch a code or create an order (maybe the API lets you bulk order, but likely one by one).
   - Send out an email to each employee.
   - As each email is sent, the corresponding reward status goes to "Sent".
   - If any email bounces (say 1 out of 200 had an outdated email), a bounce webhook comes back and that one reward is marked "Undeliverable". The HR Manager will later see 199 Sent/Delivered, 1 Failed in tracking.
10. **Recipient Redemption:** Employees begin receiving the emails in their inbox (company branded, subject "A Holiday Gift from [Company]"). They click the "Claim $50 Card" link.
    - They are taken to a branded redemption page. Suppose it's a Visa virtual card. The page might show "Your Prepaid Card Code: 1234 5678 9012 3456, Expiry 12/26" and instructions to spend online.
    - As soon as an employee clicks and views their card details, the system marks that reward "Redeemed".
11. **Tracking and Follow-up:** HR Manager checks the platform later:
    - She goes to the tracking list, filters by this campaign or date: sees e.g., "200 sent, 180 redeemed (90%), 19 pending, 1 failed".
    - For the 1 failed (maybe an ex-employee's email bounced), she can click it, get the error ("email bounced"). She decides to contact that person via phone or update their address if available. Since they're ex-employee, maybe she cancels that reward to reclaim the $50 in budget.
    - For the 19 pending (some employees haven't opened the email yet, maybe on vacation), she uses the "Send Reminder" function. The system sends a reminder email to those 19: "Reminder: don't forget your $50 gift card from [Company]".
12. **Budget Impact:** The budget page now shows $10,000 spent (or committed) out of $12,000, remaining $2,000. If one reward was cancelled, it might show $9,950 actually spent if our budget logic credits back that $50.
13. **Outcome:** Most employees redeem their gift, boosting morale. HR Manager uses the report feature later to show HR leadership: "We gave out 200 gifts, 95% redeemed within 2 weeks." Possibly correlate with a year-end survey showing high satisfaction.

**Postconditions:**

- All active employees received and (mostly) used their gifts.
- Budget correctly reflects the cost.
- The HR Manager can demonstrate the program's uptake (through redemption rate data).
- The one failed case was handled via cancellation or alternate method.

**Alternate Flow:**

- If the budget had not enough funds (say only $8k left), at step 8 the system would have blocked sending. HR Manager would either reduce recipients or request budget increase. After raising budget (Org Admin can edit from 8k to 10k) then she retries send successfully.
- If HR Manager wanted to let employees choose their gift (e.g., $50 Amazon vs $50 Target), she could have selected two options in step 2 if multi-choice feature available. Then each email link would let employee pick one. The rest of flow is similar, though tracking which choice each made could be an extra detail she can see (like 120 chose Amazon, 80 chose Target).

This scenario demonstrated:

- Bulk send flow,
- budget enforcement,
- email generation,
- redemption process,
- tracking and reminder.

### 7.2 B2B Partner Incentives Scenario

**Objective:** A Channel Marketing Manager wants to reward partner company representatives who achieved sales targets with a premium gift.

- **Actors:** Channel Marketing Manager (Program Manager role), 5 Partner Sales Reps (Recipients), Finance Manager (for approval).
- **Preconditions:**
  - Each partner rep's email is known.
  - The reward is a choice between an iPad or a $500 Visa card (multi-option reward).
  - A budget "Partner Incentives Q4" has $2,500 allocated (5 \* $500). However, Finance requires approval for any single reward > $300.
- **Trigger:** Quarter ends; Channel Manager identifies 5 partner reps to reward.

**Main Flow:**

1. **Initiate Send (Multi-option):** Channel Manager goes to Send Rewards interface.
2. **Select Reward Options:** Instead of one reward, he selects "Allow recipient to choose reward". He picks two options from catalog: "Apple iPad (worth ~$500)" and "Visa $500 Gift Card".
3. **Add Recipients:** He enters 5 email addresses (or selects contacts if saved).
4. **Message:** Writes "Congratulations on an excellent Q4! Please choose your reward as a token of our appreciation for your partnership."
5. **Budget:** Chooses "Partner Incentives Q4" budget.
6. **Send:** Clicks send. Now, because each reward is $500 which might be above an approval threshold:
   - The system detects "Reward value $500 exceeds $300 threshold" (or that sending $2,500 will exceed something).
   - It flags this for approval. Instead of immediately processing, it creates an approval request to Finance.
   - The UI shows: "Your reward distribution requires approval from Finance. It has been submitted."
7. **Approval Notification:** Finance Manager gets an email or sees a notification in the platform: "Approval needed: Partner Incentives Q4 for 5 rewards ($2,500 total)."
8. **Approval Decision:** Finance Manager logs in, goes to Approvals page, reviews details (sees recipients and cost, maybe sees reason message).
   - If all good, she clicks "Approve".
9. **Execution Post-Approval:** Once approved, the system proceeds to actually send:
   - Same as before: create reward entries for each partner rep, contact provider to reserve 5 iPads (or codes, perhaps we only finalize when they choose, so maybe we don't pre-purchase iPads, but we can pre-authorize cost).
   - Send out emails to the 5 recipients.
10. **Partner Redemption:** Each partner rep opens the email: "Choose your reward: [Button for iPad] [Button for $500 Card]".
    - They click their preferred option, go to redemption page showing whichever they picked:
      - If iPad: Perhaps it says "We'll ship an iPad to you. Please provide your shipping address." They enter address. System marks reward as redeemed (and triggers the internal process to fulfill iPad order).
      - If Visa card: It might directly display the $500 virtual card info for immediate use.
    - The system updates statuses: e.g., 3 picked iPad (status might be "Fulfillment in progress"), 2 picked Visa (status Redeemed with code given).
    - The Channel Manager can see who chose what in the tracking (e.g., list shows reward type chosen or at least notes).
    - For those who chose iPad, maybe the status is "Redeemed - pending shipment". Once the Channel Manager or an admin marks them shipped (or we integrate with shipping vendor), then final status might become "Delivered".
11. **Follow-up:** Channel Manager uses the reporting to see "5 rewards given, 100% redeemed, options chosen: 3 iPads, 2 Visa cards".
    - Budget shows $2,500 used.
    - Finance is happy it stayed within budget.

**Alternate Flow (If Finance Denied):**

- If Finance Manager had denied at step 8 (maybe thinking $500 each is too high):
  - System would notify Channel Manager of denial (with reason if provided).
  - No emails sent.
  - Channel Manager might then decide to reduce reward value or obtain higher approval via other means (maybe CFO).
  - He could change reward to $300 gift card and resend request, or get an increased budget and re-submit.

This scenario highlighted:

- Approval workflow,
- Multi-option reward redemption,
- Physical item fulfillment steps,
- Interaction between marketing and finance roles.

### 7.3 Customer Loyalty Rewards (B2C Loyalty Scenario)

**Objective:** A Product Manager automates sending a $10 coupon to customers who refer a friend, via integration with their app.

- **Actors:** Product Manager (Org Admin), Customer (Recipient), Company’s Mobile App/Backend (External System via API).
- **Preconditions:**
  - The referral program is running; the app can detect when a referral completes (friend made first purchase).
  - IncentiveHub API credentials are configured in the company's backend.
  - A budget "Referral Rewards" exists, say $5,000 for the campaign.
  - A $10 coupon code (maybe for their own service, or an Amazon $10 card) is set up in the catalog.
- **Trigger:** A customer (Alice) refers a friend, friend purchases, company's backend calls our API to send Alice a $10 reward automatically.

**Main Flow (Integration):**

1. **Event in External System:** Friend purchase triggers a function in company's backend: it prepares a request to IncentiveHub API.
2. **API Request:**
   - It makes an HTTPS POST to `https://api.incentivehub.com/v1/rewards` with payload: `{ recipient: "alice@example.com", reward: "Referral $10 Coupon", message: "Thanks for referring John! Here's $10 for you.", budget: "Referral Rewards" }` and authentication (API key or token).
3. **IncentiveHub Processing:**
   - The request hits our API gateway, passes auth (we verify API key belongs to that org).
   - The Reward API handler validates budget etc. $10 is small, likely approved automatically (no manual approval needed).
   - Creates reward entry for Alice, deducts $10 from "Referral Rewards" budget.
   - Because this is a small single send, it might synchronously get a code (if the reward is an internal coupon, maybe the company provided a list of coupon codes to our catalog or we generate one).
   - Then calls Notification service to send out the email to Alice.
   - Returns a response to company's backend, e.g., `{"status": "queued", "rewardId": 12345}` (or status "sent" if done instantly).
4. **External System Feedback:** The company's backend receives the response and logs it. It might also subscribe to a webhook for redemption (not critical here).
5. **Reward Delivery:**
   - IncentiveHub sends Alice an email: "You earned a $10 coupon for referring a friend! Use code XYZ10 for $10 off."
   - (If integrated with their app, we might also send a webhook to their app or an email to appear in-app as well, but primary is email).
6. **Redemption:** Alice sees the email, uses the code on her next purchase. That redemption might actually happen on company's side (since it's their coupon code).
   - If it's our gift card, we can track redemption if we gave a link.
   - But since this might be a company coupon, they handle redemption. We might just mark it as delivered.
   - Possibly, the company's app calls our API to mark it used after Alice uses it (if they want the tracking in one place).
7. **Tracking:** The Product Manager can later look at IncentiveHub dashboard:
   - Sees that X number of $10 coupons have been sent via the API (maybe labeled under "Referral Program" campaign).
   - Redemption might not be tracked if it's an external code usage, but they can see how many were sent and possibly how many customers clicked if we had email open tracking.
   - However, because it's their own coupon, they can reconcile usage in their commerce system.
8. **Budget Monitoring:** If referrals explode and the $5,000 budget is almost used, the system would start rejecting further sends or sending approval requests.
   - Product Manager might get an alert "Referral Rewards budget 90% used".
   - They then increase it or decide to cut off referrals until next month.

**Alternate Flow:**

- If the company's app wanted to show the reward in-app instead of email:
  - Instead of us emailing Alice, their backend might call our API to get a code but not have us email it. They then show it in Alice's app profile.
  - We would support that by an API call like `POST /rewards?deliver=false` or a special endpoint to just generate and return a code.
  - Then their app shows "You earned $10 off! Use code XYZ10".
  - In such case, our system just records a reward and marks it delivered because we returned code to them. Possibly no email triggered.
  - This approach is possible with our integration flexibility, not detailed in core requirements but architecture allows it.

This scenario demonstrates:

- The integration capabilities via API,
- automation (no human in loop on our side),
- handling large number of small transactions smoothly, -_(Continued)_

...

**Outcome:** This automated workflow shows how IncentiveHub can seamlessly integrate with the company's referral system. Alice receives her reward promptly without manual intervention. The Product Manager can monitor how many referral coupons have been distributed and ensure the budget is respected. The integration and automation improve efficiency and customer satisfaction (immediate rewards).

**This scenario demonstrates** the platform's API use and automated reward delivery: the company's system triggers rewards in real-time, IncentiveHub handles fulfillment (generating codes, sending notifications) and enforces budget limits, providing a hands-off solution for the product team.

### 7.4 Research Survey Incentives Scenario

**Objective:** A Research Coordinator wants to reward people for completing an online survey with a $20 e-gift card, distributing these rewards in bulk after the survey closes.

- **Actors:** Research Coordinator (Program Manager role), Survey Participants (Recipients).
- **Preconditions:**
  - 100 participants completed the survey and provided their email addresses for the incentive.
  - A budget "Survey Q1 Incentives" of $2,000 is allocated.
  - $20 Amazon gift card is available in catalog for that amount.
- **Trigger:** Survey period ends; coordinator needs to send all 100 rewards.

**Main Flow:**

1. **Data Preparation:** The coordinator exports the list of participant emails from the survey platform (e.g., a CSV with 100 emails).
2. **Bulk Send:** In IncentiveHub, the coordinator chooses the $20 Amazon gift card from the catalog, uploads the CSV of 100 emails, writes a message like "Thank you for participating in our survey! Enjoy this $20 Amazon gift card as a token of our appreciation." and selects the "Survey Q1 Incentives" budget.
3. **Send & Process:** They hit send. The system verifies budget ($2,000 total needed, exactly matching budget, so it's okay). It creates 100 reward entries and queues emails to each.
4. **Email Delivery:** Emails are sent out to all participants with their $20 Amazon code or a link to claim it. (We might choose to include the code directly in this case for simplicity, or a link to a claim page where they see the code — either way).
5. **Redemption:** Participants receive the email. Most will click the link or copy the code to use on Amazon. When they click the claim link (if used), the system marks their reward redeemed. If the code was given in email without link, we rely on the gift card provider's usage for redemption status (which we might not track in real-time; it's okay if we don’t get confirmation for all, since it's a one-time distribution).
6. **Tracking:** The coordinator checks IncentiveHub after a week:
   - Sees maybe 85 of 100 have redeemed (85%), 15 pending. She decides those 15 might not ever redeem (some people ignore small rewards). She can choose to send a reminder to those 15 through the platform or just let it be.
   - The budget shows $2,000 spent (if budget counts on send). If they set budget to count on redemption and only 85 redeemed after a long time, maybe they'd consider $1,700 spent and $300 returned — but typically they'd count all as expense anyway.
7. **Follow-up:** She exports a report of survey incentives showing distribution and redemption rate to include in her research project documentation (this demonstrates participant compensation was handled).

**Alternate:** If anonymity was crucial (survey is anonymous), the researcher might have collected contact emails separately purely for reward. The process remains same but ensures that connecting survey answers to emails is not done in our system — which it isn't, we just send to the list given.

**Outcome:** All qualifying participants get their reward, improving goodwill and increasing likelihood of future participation. The researcher meets the obligation to compensate, and the platform made it easy to do so in one batch with trackable results.

---

These use cases illustrate how IncentiveHub handles various scenarios: scheduled bulk distributions, on-demand API-triggered sends, multi-option rewards with approval needs, and bulk research incentives. In each case, the system fulfills the requirements: ensuring correct budget usage, delivering rewards promptly (and via the desired channel), and providing feedback to the senders about the status and effectiveness of their incentives.

## 8. Appendix

This appendix contains supplementary reference information that supports the main document, including detailed tables and a glossary of terms used.

### 8.1 Role Permissions Matrix (Detailed)

The following table expands on Table 3.6.1, providing a comprehensive view of what actions each default role can perform in the system:

| **Action / Feature**                   |                                                    **Org Admin**                                                    |                           **Program Manager**                           |                           **Finance Manager**                           |                 **Viewer**                  |
| -------------------------------------- | :-----------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------: | :---------------------------------------------------------------------: | :-----------------------------------------: |
| **User Management**                    |                                Create/Edit/Deactivate any user in org; assign roles.                                |       No (cannot manage users; can only edit their own profile).        |                                   No.                                   |                     No.                     |
| **Configure SSO/Integrations**         |                                       Yes (full access to org-wide settings).                                       |                                   No.                                   |                                   No.                                   |                     No.                     |
| **View Org Settings**                  |                                                        Yes.                                                         |     Maybe (could view some settings if allowed, but typically no).      |            Maybe (could view budgets config but not change).            |                     No.                     |
| **Create Budget**                      |                                                        Yes.                                                         |               Possibly (could request, but not finalize).               |                  Yes (likely responsible for budgets).                  |                     No.                     |
| **Edit Budget**                        |                                                        Yes.                                                         | Possibly propose changes (workflow), but not finalize without approval. |                                  Yes.                                   |                     No.                     |
| **Approve Budget/Reward Requests**     |                                               Yes (can approve any).                                                |                      No (they initiate requests).                       |                    Yes (approve financial requests).                    |                     No.                     |
| **Send Single Reward**                 |                                               Yes (to anyone in org).                                               |             Yes (to recipients relevant to their programs).             |       Typically no (not their role, unless also have PM rights).        |                     No.                     |
| **Send Bulk Rewards**                  |                                                        Yes.                                                         |                       Yes (for their campaigns).                        |             No (unless assisting someone, but normally no).             |                     No.                     |
| **Schedule Rewards**                   |                                                        Yes.                                                         |                                  Yes.                                   |                                   No.                                   |                     No.                     |
| **Cancel/Modify Sent Reward**          |                                     Yes (can cancel any pending reward in org).                                     |                   Yes (can cancel rewards they sent).                   |                           No (not involved).                            |                     No.                     |
| **View All Rewards (Tracking)**        |                                                Yes (all campaigns).                                                 |    Yes (their own campaigns; possibly those of team if configured).     |              Yes (likely all, because they monitor spend).              |   Possibly limited view (summary stats).    |
| **View Reports/Analytics**             |                                                   Yes (full org).                                                   |    Yes (for programs they have access to; maybe summary of others).     |        Yes (especially spend and redemption reports across org).        | Yes (read-only high-level data if granted). |
| **Access Audit Logs**                  |                                                Yes (org audit logs).                                                |                                   No.                                   | Typically no (maybe can view budget log entries pertaining to finance). |                     No.                     |
| **Manage Catalog (add custom reward)** |                                                        Yes.                                                         |    Maybe (could submit a custom reward request that Admin approves).    |                                   No.                                   |                     No.                     |
| **Manage Templates (Email text)**      |                                                        Yes.                                                         |            Possibly edit messages for their campaigns only.             |                                   No.                                   |                     No.                     |
| **Impersonate User**                   | Platform Super-Admin only (Org Admin of client cannot impersonate others, except maybe view as Viewer for testing). |                                   No.                                   |                                   No.                                   |                     No.                     |
| **API Access**                         |                                      Yes (can generate API keys for the org).                                       |       Maybe (if allowed to use API for their program automation).       |                       Typically no (not needed).                        |                     No.                     |

_(The exact distribution of permissions can be configured per organization, but the above represents the default intention of each role.)_

### 8.2 Reward Status Lifecycle Table

This table recaps the reward lifecycle states and transitions for reference (as covered in section 3.3):

| **Status**               | **Meaning**                                                                                      | **Triggers/Next Steps**                                                                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pending** _(optional)_ | (Sometimes used to mean created but not yet sent, e.g., if awaiting approval or scheduled.)      | → Sent (when approved or time reached) or → Cancelled (if not proceeding).                                                                                          |
| **Sent**                 | Reward notification dispatched (email/SMS sent).                                                 | → Delivered (if confirmation from channel) <br> → Undeliverable (if bounce/fail) <br> → Opened (if tracking detect) <br> → Redeemed (if immediate redeem via link). |
| **Delivered**            | Delivery confirmed (e.g., email did not bounce). It implies the recipient should have it.        | → Opened (if recipient engages) <br> → Redeemed <br> → Expired.                                                                                                     |
| **Opened**               | Recipient opened the notification or clicked link. Indicates interest.                           | → Redeemed (likely next) <br> → Expired (if never completed redemption).                                                                                            |
| **Redeemed**             | Reward claimed/used by recipient. Final successful state.                                        | (No further transitions; reward is completed.)                                                                                                                      |
| **Undeliverable/Failed** | Delivery failed (email bounced, SMS failed, or provider couldn't supply reward).                 | → Possibly Resend (if user corrects issue, effectively creating new send event) or Cancelled.                                                                       |
| **Cancelled**            | Reward was invalidated (by admin or system) before redemption (or after a failure). Final state. | (No further transitions; if needed, admin could issue a new reward separately.)                                                                                     |
| **Expired**              | Recipient did not redeem within allowed time; reward offer expired. Final state.                 | (No further transitions; admin could manually reissue if they decide to in a new entry.)                                                                            |

### 8.3 Glossary

- **Org (Organization/Tenant):** A client company or unit using the platform, with its own users, rewards, budgets.
- **Recipient:** An end user who receives a reward (employee, customer, etc.).
- **Reward Instance:** A specific reward sent to a particular recipient (with unique code/link).
- **Campaign/Program:** A defined initiative or context for sending rewards (e.g., “Holiday 2025 Gifts” or “Referral Program Q1”). Used for grouping and reporting.
- **Provider (Reward Provider):** External service that actually supplies the reward value (gift card vendor, etc.).
- **Webhook:** A mechanism where one system sends HTTP requests to another when certain events happen (used for notifications like email bounce or redemption events).
- **SLA (Service Level Agreement):** A commitment for uptime or performance (e.g., 99.9% uptime).
- **PII:** Personally Identifiable Information (like names, emails). Subject to privacy laws.
- **SOC 2:** A security and trust auditing standard for service organizations. Having SOC 2 compliance means following strict policies in security, availability, etc.
- **API Key:** A secret token used by external systems to authenticate with our API.
- **JWT (JSON Web Token):** A format for tokens often used for auth, containing claims about user identity and signed to ensure integrity.
- **IdP (Identity Provider):** The SSO server that authenticates users (like Okta, Azure AD).
- **SP (Service Provider):** In SSO terms, our platform is the Service Provider that delegates auth to IdP.
- **CSV (Comma-Separated Values):** A simple file format for tabular data, often used for imports/exports (e.g., recipient lists).
- **Pen Test:** Penetration Test, a security assessment where testers try to find vulnerabilities.

### 8.4 Sample Email Template (for reference)

Below is an example of what a reward notification email might look like, including placeholders that the system would replace:

```
Subject: You’ve earned a reward from {{CompanyName}}!

Hello {{RecipientName}},

Thank you for {{Reason or Campaign Name}}. As a token of our appreciation, {{CompanyName}} is pleased to give you {{RewardName}}.

{{#if RewardCode}}
Your gift code: {{RewardCode}}
Use this code at {{RewardRedemptionInstructions}} to redeem your reward.
{{else}}
Click the button below to claim your reward:
{{RedemptionLinkButton}}
{{/if}}

{{PersonalMessageFromSender}}

If you have any questions or trouble redeeming your reward, please contact us at {{SupportEmail}}.

Thanks again,
The {{CompanyName}} Team

( {{CompanyName}} – {{CompanyAddress}} )
```

_(This template would be populated by the Notification Service for each email. The logic shown (Handle if we directly have a code vs providing a link) is just illustrative.)_

---

**End of Document.**
