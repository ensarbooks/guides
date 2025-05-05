

# **Software Requirements Specification (SRS) – E‑Commerce Analytics SaaS for Shopify**

## **1. Introduction**

**Purpose:** This document defines the comprehensive requirements for a Software-as-a-Service (SaaS) product in the **E-Commerce Analytics** category targeted at Shopify users. It outlines the functional, non-functional, UI/UX, technical, and other requirements needed to design and implement a platform that provides **e-commerce-specific KPIs and analytics**. The goal is to ensure Shopify merchants can easily integrate the software and gain insights through **dashboards**, **multi-channel sales analysis**, **web analytics**, and **marketing campaign tracking**.

**Scope:** The product (hereafter referred to as “the system”) will connect with a merchant’s Shopify store (via built-in integration or APIs) to automatically gather data on sales, customers, and website behavior. It will also ingest data from other sales channels (social media shops, marketplaces like Amazon/eBay) and marketing platforms (Facebook/Meta Ads, Google Ads, email marketing services) to provide a **unified analytics dashboard**. Key performance indicators (KPIs) such as conversion rate, average order value, cart abandonment rate, etc., will be tracked and visualized. The system covers data collection, storage, processing, analytics computations, and presenting results in an intuitive UI. It will **not** handle transaction processing or act as an e-commerce storefront; it purely focuses on analytics and reporting.

**Definitions, Acronyms, and Abbreviations:**

* **SaaS:** Software as a Service – a cloud-based application accessed via web browser.
* **Shopify:** A leading e-commerce platform that merchants use to host online stores. Our system will integrate with Shopify’s APIs.
* **KPI:** Key Performance Indicator – a measurable value that indicates how well an e-commerce business is achieving key objectives (e.g., conversion rate, revenue).
* **Conversion Rate:** The percentage of website visits that result in a purchase (orders/visits).
* **Average Order Value (AOV):** The average dollar amount spent per order (total revenue / number of orders).
* **Cart Abandonment Rate:** Percentage of shopping carts created that were not completed with a purchase.
* **Customer Lifetime Value (CLV/CLTV):** Projected revenue a business will earn from a customer over the entire lifespan of their relationship.
* **Multi-Channel:** Selling or marketing across multiple platforms/channels (e.g., an online Shopify store, social media, marketplaces).
* **Attribution Model:** A rule or set of rules that determines how credit for sales/conversions is assigned to touchpoints in the customer journey (e.g., first-touch, last-touch, linear multi-touch).
* **GDPR:** General Data Protection Regulation – EU law on data privacy and security, which the system must comply with regarding personal data.
* **RESTful API:** An application programming interface following REST principles, enabling external systems to interact with our system (for data ingestion or retrieval).
* **Webhook:** A mechanism for one system to send real-time data to another via HTTP callbacks (used by Shopify to push events like order creation to our system).

**Overview:** Following this introduction, Section 2 details **Functional Requirements** (the features and functions the system will provide). Section 3 specifies **Non-Functional Requirements** (performance, security, etc.). Section 4 covers **UI/UX Requirements** including design guidelines and internationalization. Section 5 outlines **Technical Requirements** such as integration details and system architecture. Section 6 defines **User Roles & Permissions**. Section 7 addresses **Data Storage and Reporting** mechanisms. Diagrams and tables are included to illustrate key concepts (e.g., dashboard layout, data flow architecture, role permissions).

## **2. Functional Requirements**

The functional requirements describe what the system **shall do** – the capabilities and features expected. The product focuses on delivering e-commerce-specific analytics, hence requirements span KPI tracking, multi-channel data analysis, marketing integrations, and web analytics.

### **2.1 E-Commerce KPI Tracking**

The system shall provide comprehensive tracking of key performance indicators (KPIs) specific to e-commerce. This includes capturing data from Shopify (and other integrated sources) and computing metrics that help merchants understand their sales performance, customer behavior, and store health. Below is a list of core e-commerce KPIs the system will track, along with descriptions and how they are derived:

**Table 1 – Key E-Commerce Metrics to Track**

| **KPI Metric**                                      | **Description**                                                                                                                                                                                                                                                                                                                                                                            | **Calculation / Source**                                                                                                                                                                                                                                                                                                                                                                |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sales Conversion Rate**                           | The percentage of store visitors (sessions) that result in a completed order. It indicates how effectively the site converts traffic into sales. A typical e-commerce conversion rate is around 2-3% (Shopify stores average \~1.4% with 3.2%+ being top 20%).                                                                                                                             | **Formula:** (Number of Orders / Number of Website Sessions) × 100%. For example, 50 orders out of 1,000 visits = 5% conversion. Source data from Shopify “Orders” count and web analytics for session count.                                                                                                                                                                           |
| **Average Order Value (AOV)**                       | The average monetary value of each customer order. This helps assess how much customers spend on average per transaction. Higher AOV means more revenue per order.                                                                                                                                                                                                                         | **Formula:** Total Revenue / Number of Orders over a given period. For instance, \$50,000 revenue / 1,000 orders = \$50 AOV. Data from Shopify orders (sum of order totals) divided by order count.                                                                                                                                                                                     |
| **Customer Lifetime Value (CLV)**                   | An estimate of the total revenue a business can expect from a single customer account over the life of the customer relationship. This guides marketing spend and retention strategies.                                                                                                                                                                                                    | **Formula (simplified):** Average Order Value × Average Purchase Frequency × Average Customer Lifespan (in number of orders or time). For example, if AOV = \$50, customer orders 3 times a year, and stays \~2 years, CLV ≈ \$50×3×2 = \$300. The system will calculate this based on historical customer purchase data from Shopify (total spend per customer) and predictive models. |
| **Cart Abandonment Rate**                           | The percentage of shopping carts that are abandoned (items added to cart but not purchased). A high abandonment rate indicates issues in the checkout process or buyer hesitation. Industry studies show an average cart abandonment of \~68.8%, often even 70%+, meaning the majority of initiated carts do not convert to orders. Reducing this metric can immediately increase revenue. | **Formula:** (1 – (Number of Completed Purchases / Number of Shopping Carts Created)) × 100%. For example, if 200 carts were created and 45 resulted in purchases, abandonment = 1 – (45/200) = 77.5%. The system will capture “cart created” events (via web analytics or Shopify’s cart data if available) and completed orders to compute this.                                      |
| **Repeat Purchase Rate**                            | The percentage of customers who make more than one purchase (customer retention indicator). It shows loyalty and satisfaction.                                                                                                                                                                                                                                                             | **Formula:** (Number of Customers with 2+ purchases / Total Number of Customers) × 100%. Source from Shopify customer and order records. Also related to **Returning Customer Rate** (Shopify provides this as the proportion of orders from returning vs new customers).                                                                                                               |
| **Customer Acquisition Cost (CAC)**                 | The average cost to acquire a new customer. This is crucial for evaluating marketing efficiency in conjunction with CLV.                                                                                                                                                                                                                                                                   | **Formula:** Total Marketing Spend on customer acquisition / Number of New Customers acquired. The system will integrate marketing spend data (from ad platforms) and track new customer counts (via Shopify customer records) over the same period. For example, if \$5000 spent on ads in a month yielded 250 new customers, CAC = \$20.                                              |
| **Gross Sales & Net Sales**                         | Gross sales = total sales revenue before deductions. Net sales = revenue after refunds, discounts, returns. These indicate overall revenue performance.                                                                                                                                                                                                                                    | **Calculation:** The system will sum order totals (gross) from Shopify. Net sales = gross sales minus refunds and returns (which are tracked via Shopify orders/refunds data). The system shall display both, and the difference can indicate how returns impact revenue.                                                                                                               |
| **Gross Profit Margin**                             | Profitability metric: portion of revenue left after cost of goods sold (COGS) and direct fees. If product cost data is available, this can be calculated.                                                                                                                                                                                                                                  | **Formula:** ((Total Revenue – COGS) / Total Revenue) × 100%. *Note:* Requires input of product costs. The system may allow merchants to input COGS per product or integrate with inventory management for cost data. If not available, this metric may be omitted or marked as N/A.                                                                                                    |
| **Traffic & Engagement Metrics**                    | Various metrics about site traffic and user engagement that affect sales funnel. See *Web Analytics* section for details, but key ones include: **Total Visits/Sessions**, **Bounce Rate** (percent leaving immediately), **Average Session Duration**, **Pages per Session**, and **Top Landing/Exit Pages**. These are leading indicators for the funnel before conversion.              | **Source:** Web analytics tracking (either via integration with Google Analytics or using the system’s own tracking script on the storefront). E.g., Bounce Rate = % of single-page sessions (no interaction beyond landing). These help diagnose where customers drop off before purchasing.                                                                                           |
| **Funnel Conversion Metrics**                       | Step-wise conversion rates for stages in the shopping funnel: e.g., Product View → Add to Cart → Checkout Start → Purchase. This helps pinpoint where users drop off.                                                                                                                                                                                                                      | **Calculation:** The system will track counts at each stage and compute ratios between stages. For example: *Add-to-Cart Rate* = (Carts Created / Product Views)×100%; *Checkout Completion Rate* = (Orders / Checkouts Started)×100%. Such funnel metrics highlight friction points (e.g., if many add to cart but few check out, checkout process may need improvement).              |
| **Top Products and Categories**                     | Identification of best and worst performing products or categories by sales, and their metrics. Helps in inventory and marketing focus.                                                                                                                                                                                                                                                    | **Data:** From Shopify product and order line items. The system shall list top N products by units sold, revenue, or profit. Also track product-specific metrics like conversion rate (views to purchases per product), average price, etc.                                                                                                                                             |
| **Inventory Turnover & Stock-Outs** (if applicable) | Metrics related to inventory if relevant to analytics: e.g., units sold per day, inventory remaining, stock-out events. (Shopify provides some inventory data via reports).                                                                                                                                                                                                                | **Data:** The system can pull inventory counts and track how quickly products sell (average inventory sold per day). While core focus is analytics, basic inventory analytics (like month-end stock snapshot) can be included for completeness.                                                                                                                                         |

*Rationale:* By tracking the above KPIs, merchants can monitor store performance in real-time and historically. For example, tracking **conversion rate** and **abandonment** together provides insight: if traffic is high but conversion is low, something is wrong in converting visitors to buyers (perhaps a UX issue or irrelevant traffic). If **AOV** increases after a promotion (upselling), that strategy is validated. Monitoring **customer retention metrics** (repeat rate, CLV) alongside **acquisition metrics** (CAC) shows if the business is sustainably acquiring valuable customers (e.g., CLV should ideally exceed CAC). Each KPI will be updateable in near real-time (depending on data sync frequency) on the dashboards (see Section 4 UI/UX for dashboard specifics).

The system shall allow users to **filter** these KPIs by various dimensions such as date range (e.g., view metrics for last 7 days, last month, custom range), by sales channel (online store vs other channels), by customer segments (new vs returning customers), and by product or category (where applicable). This enables drilled-down analysis, for example: conversion rate for mobile vs desktop traffic, or AOV for a specific product category.

Additionally, merchants will be able to set **goals or benchmarks** for certain KPIs and have the system indicate progress (e.g., highlight in green if conversion rate meets a target or in red if below). The system might incorporate industry benchmarks as reference – for instance, flagging if conversion rate falls far below industry average (\~2.5%) or if cart abandonment is higher than typical \~70%.

**Requirement F-1:** *The system shall compute and display all relevant e-commerce KPIs (including but not limited to those listed in Table 1) using data from Shopify and integrated sources, updated at least daily (preferably in near real-time). Calculations should follow standard industry definitions and formulae for each metric to ensure accuracy and familiarity to users.* Each KPI must have an on-screen description or tooltip explaining what it measures and how it’s calculated, for user clarity.

**Requirement F-2:** *The system shall provide comparative views for KPIs over time (trends).* For example, line charts for daily conversion rate over a selected period, or month-over-month comparisons of revenue, etc. This includes year-over-year comparisons for seasonal businesses, if data is available for previous year.

**Requirement F-3:** *The system shall allow users to configure alerts for certain KPI thresholds.* (E.g., send an email or in-app alert if daily sales fall below X, or if cart abandonment rises above Y%). This ensures merchants can proactively respond to anomalies.

### **2.2 Multi-Channel Sales Analytics & Attribution**

Modern e-commerce occurs across multiple channels. A Shopify merchant might sell through their online Shopify store, but also list products on marketplaces (Amazon, eBay), sell via social media shops (Instagram Shop, Facebook Store), or even have offline sales that can be imported. The system shall aggregate and analyze sales data from multiple channels to give a **holistic view** of the business.

**Multi-Channel Data Integration:** The system will support integrating sales data from:

* **Shopify Online Store:** (primary source) via direct API connection or Shopify’s built-in analytics.
* **Social Commerce Channels:** e.g. Facebook Shop/Instagram (which might be managed via Facebook Commerce Manager), Pinterest shopping, TikTok store, etc. These can be integrated via their APIs or via Shopify if Shopify is the source of truth for those orders (Shopify supports some social channel integrations that sync orders back to Shopify).
* **Marketplaces:** e.g. Amazon Marketplace, eBay, Etsy. This requires connecting to each marketplace’s API or using a third-party aggregator. Initially, the focus will be on Shopify (which could also capture some marketplace sales if the merchant uses Shopify’s Amazon integration). If not, future versions can incorporate connectors to fetch orders from these platforms.
* **Offline/POS:** If the merchant uses Shopify POS or other channels, those could also be considered (though not explicitly requested, but to note completeness).

**Unified Dashboard:** All sales from these channels should be combined for an **overall sales view**, but also **attributable by channel**. For example, the dashboard might show total revenue, and then a breakdown by channel: *Shopify Store vs Amazon vs Facebook*, etc., both in numerical form and in charts (pie or bar chart for channel contribution).

**Requirement F-4:** *The system shall consolidate sales, orders, and customer data from all connected channels into a unified data model.* Each order record should carry a “Channel” attribute (e.g., Shopify, Amazon, etc.). Users should be able to filter any metric by channel or view side-by-side performance per channel.

**Sales by Channel:** Metrics like revenue, order count, units sold, and conversion rate should be available per channel. For example, one could view “Revenue by Channel” for the last month: Shopify \$X (Y%), Amazon \$Z (W%), etc., and possibly see trends in each. **Figure 1** below illustrates an example dashboard panel breaking down revenue by channel and device:

&#x20;*Figure 1: Example Dashboard – Multi-channel Overview.* *This sample shows a dashboard with KPIs including a “Revenue by Channel” breakdown (Direct, Organic, Referral, Email, Paid Search etc.), a sales funnel from sessions to orders, and other widgets like Sales Breakdown and Abandoned Carts. Our system’s dashboard will have similar multi-channel and funnel visualizations.*

As shown in Figure 1, the system will present multi-channel data in a clear way. For instance, an **Overall Sales Funnel** might be displayed (total sessions → total carts → total orders across all channels, as percentages), and next to it a **Revenue by Channel** chart to identify which channels drive the most revenue (with percentages of contribution).

**Attribution Models:** A key requirement is to analyze the **performance of marketing channels in driving sales**, i.e., attribution. Not all customer journeys are single-touch (e.g., a customer might first click a Facebook ad, later come via email, then direct to site and purchase). The system shall support **multiple attribution models** for crediting conversions to marketing efforts:

* **Last-Touch Attribution:** Credit the last touchpoint (e.g., the channel of the visit that immediately resulted in the order) for the sale. (This is the simplest and often default model, used in many analytics by default).
* **First-Touch Attribution:** Credit the channel where the customer’s first interaction occurred (useful to see what initially brought them in).
* **Linear Attribution:** Distribute credit equally among all touchpoints in the customer’s journey to purchase.
* **Time-Decay Attribution:** Give more weight to touchpoints closer in time to the conversion, and less to earlier ones.
* **Position-Based (U-Shaped) Attribution:** Give significant weight to first and last touch, and smaller weight to the middle interactions.
* (If possible) **Custom Attribution:** Allow custom weightings or algorithmic attribution, though this may be advanced; initially the above standard models suffice.

These models help answer which marketing channels are truly contributing to sales. For instance, **multi-touch attribution** recognizes that “every touchpoint a customer has with your brand can influence their decision to convert”. The system’s attribution analysis will help merchants determine the value of each channel/touchpoint in the multi-channel customer journey.

**Requirement F-5:** *The system shall track customer journeys across marketing channels and apply multiple attribution models to assign credit for conversions.* This means if the data is available (via integrated marketing tools and web analytics), each order can be linked to a customer journey path (sequence of touches). The system should then be able to output reports like “Marketing Attribution Report” under different models. For example, under First-Touch model, Paid Search might be credited with 50% of sales, whereas under Last-Touch, Email gets 50%. The UI will allow switching the attribution model to see how credit distribution changes.

To facilitate this, the system will rely on tracking parameters (like UTM codes in URLs that identify source/medium/campaign for visits) and possibly a user identifier to stitch sessions together. For logged-in users, an ID can tie their sessions; for anonymous, cookies or fingerprinting can attribute touches until conversion. The system will integrate with Shopify’s order attribution (Shopify captures referral source of an order if via last-click), and augment it with our own tracking for multi-touch.

**Multichannel Customer Analytics:** Beyond just sales, the system should identify if customers overlap across channels. For example, a customer might buy on Amazon and also on the Shopify site. If the merchant can provide a way to link those (e.g., via email or name matching), the system should unify such customer profiles to accurately calculate CLV and avoid double-counting as separate people. (This might be a stretch goal, but conceptually included).

**Channel-Specific Metrics:** Each channel might have unique metrics:

* For example, Amazon might provide **Buy Box win rate** or seller rating – but those may be beyond scope. We mainly focus on sales, orders, etc., across channels.
* Social channels might include metrics like followers or engagement leading to site visits; those are more marketing metrics, possibly covered in integration with marketing tools.

For simplicity, initial multi-channel analytics will center on sales and traffic attribution. Extended channel-specific analytics can be future enhancements.

**Requirement F-6:** *The system shall enable comparison of channel performance and ROI.* This includes showing metrics like **Cost per Acquisition by channel** (if ad spend per channel is known) and **Return on Ad Spend (ROAS)** for paid channels. For instance, if Facebook Ads cost \$500 in a period and drove \$2000 in attributed sales, ROAS = 4.0 (400%). Similarly, for each channel or campaign, the platform should display how much revenue was generated vs cost.

**Attribution Reporting Example:** A **Marketing Performance Dashboard** might be provided (either built-in or user-generated) that shows, say, a table of campaigns with columns for Impressions, Clicks, Spend, Orders Attributed, Revenue Attributed, and ROAS under a chosen attribution model. Graphs could plot cumulative spend vs revenue for key channels over time, etc.

*(For UI perspective, Section 4 will detail an example of how attribution visuals could look, potentially showing toggling between models. But functionally, the calculations and data linking are required.)*

### **2.3 Integration with Marketing & Advertising Tools**

To fully understand marketing effectiveness and campaign performance, the system must integrate with external **marketing and advertising platforms**. Specifically, it should support:

* **Meta (Facebook/Instagram) Ads Integration:** The system shall connect to Meta’s marketing API (Facebook Graph API) to pull in advertising data for the merchant’s campaigns. This includes campaign names, spend, impressions, clicks, click-through-rate (CTR), conversions (if tracked via Meta Pixel or offline conversions), etc. By integrating this, the dashboard can show how Facebook/Instagram ads are performing and tie that data to actual Shopify sales. For example, the system can display **CTR of Facebook ads** and conversion metrics side by side; recall that typical CTRs might be \~1.66% for search ads or \~0.45% for display, and \~2% for email – giving context to the merchant’s CTR figures.

  *Requirement F-7a:* *The system shall allow the user to authenticate/connect their Facebook Ads account (via OAuth) and select which ad accounts/campaigns to import.* It will then regularly fetch data (daily or more frequently via API) on spend, impressions, clicks, conversions for those campaigns.

* **Google Ads Integration:** Similarly, connect to Google Ads API to retrieve campaign metrics (spend, impressions, clicks, conversions value). Google Ads data will enable calculating metrics like **Cost per Click (CPC)** and **Cost per Conversion** and linking Google Ads campaigns to resulting revenue in Shopify (if UTM parameters or Google Analytics conversion tracking is used).

  *Requirement F-7b:* *The system shall integrate with Google Ads, pulling key metrics for campaigns and enabling linking of Google Ads campaigns to e-commerce conversions.* For instance, if UTM source=google and campaign X is present on orders, the system should attribute those orders (or fractions, if multi-touch) to campaign X. Additionally, display metrics like campaign ROI, or suggest which keywords are driving profitable sales.

* **Email Marketing Platform Integration:** E-commerce marketing heavily uses email (newsletters, abandoned cart emails, post-purchase follow-ups). The system should integrate with popular email marketing tools such as **Mailchimp, Klaviyo, Constant Contact, SendinBlue, or Shopify Email**. Key metrics to import: campaign name, send date, number of emails sent, open rate, click-through rate (CTR), and any provided conversion stats (some email tools track if a recipient purchased after clicking, via integration or UTM). If direct conversion tracking isn’t available, the system can rely on matching UTM campaign parameters or coupon codes used.

  For example, an **Email Campaign Performance** dashboard might show for each campaign email: Open Rate (e.g. 20%), CTR (e.g. 3%), and attributed orders/revenue. The Coupler.io example in their blog showed a Mailchimp performance dashboard which tracked the funnel from emails sent → opened → clicked → revenue. We aim to provide similar insights natively.

  *Requirement F-7c:* *The system shall integrate with at least one email marketing service (initially) – e.g., via Mailchimp’s API or Klaviyo’s API – to fetch campaign performance data. It shall correlate email campaigns with Shopify orders (via tracking parameters or dedicated discount codes).* For instance, if an email campaign contained a specific coupon code, the system can detect orders using that code and attribute that revenue to the email. Or if the email links included `utm_campaign` parameters, the system uses those to attribute any sessions/orders to the email campaign.

* **Google Analytics (GA) / Web Analytics Integration:** (This intersects with the next section on Web Analytics). The system may either integrate with Google Analytics (GA4) or provide its own tracking. If integrating with GA, it can import website traffic and behavior metrics, as well as multi-channel funnel data from GA. However, GA might already provide some e-commerce tracking – the value here is combining it with other sources. If the user has GA4 configured for their Shopify store, the system could use GA’s API to pull metrics like total users, sessions by source, etc. Alternatively, to reduce dependence on GA (and avoid sampling issues or GA’s complex UI for the merchant), our system might implement its own tracking script for first-party analytics (discussed later).

  *Requirement F-7d:* *The system should optionally integrate with Google Analytics to enrich data (for example, to get website traffic by source if not directly tracked). However, this is optional if a built-in web tracking solution is provided.* If GA integration is enabled, it should fetch data such as sessions by traffic source, bounce rate, etc., to display alongside Shopify data.

* **Other Marketing Integrations:** Future or additional integrations could include:

  * **Social Media Insights:** e.g., connect to Instagram Insights or Facebook Page to track engagement metrics – useful if correlating social engagement with site traffic.
  * **SEO/Google Search Console:** to see if organic search impressions/clicks correlate with sales (though more of an SEO tool, can be valuable).
  * **Affiliate Platforms:** if the merchant uses affiliate marketing, integrating those can show referrals and their conversion.
  * **Ad networks like Pinterest Ads, Twitter Ads, TikTok Ads:** depending on user base needs. The architecture should be extensible to add these later without major overhaul (see Non-functional: Extensibility).

**Campaign and Promotion Tracking:** In addition to external ads and emails, merchants run on-site promotions (discount codes, flash sales, etc.). The system should track the performance of these promotions:

* E.g., a summary of a specific discount code: how many uses, total discount given, incremental sales generated. Since Shopify records discount code usage per order, this can be pulled via the API.
* If a promotion has a time window (like “Black Friday Sale” with automatic discounts), the system should allow tagging that period or those orders to measure the uplift in sales, etc.

*Requirement F-8:* *The system shall provide a way to track on-site marketing campaigns or promotions.* This might be as simple as filtering by a given discount code or tag to produce metrics, or a specialized report for promotions. For example, an **“Abandoned Cart Recovery Email”** campaign’s effectiveness: if Shopify flows or an email tool sends emails to recover carts, how many were converted due to those emails (Shopify might mark if an order was from an abandoned cart recovery link).

**Data Refresh and Sync Frequency:** Marketing and ad data should be fetched frequently enough to be actionable. Daily sync is minimum; more frequent (e.g., every hour or real-time webhooks if available) is ideal for near-real-time dashboards (though ad platforms often have slight delays in reporting conversions). The system should indicate the last updated time for each data source to manage expectations.

**Integration Setup & Configuration:**

* Users should be able to connect these external accounts easily from a settings area. E.g., “Connect Facebook Ads” → OAuth to Facebook, select ad account.
* The system shall securely store API credentials or tokens needed to fetch data (see Security for how).
* The UI should allow the user to select which campaigns or data to include/exclude (for instance, maybe they only want certain campaigns tracked, though likely all).
* If a user doesn’t use some platform, that integration can remain unconnected and those sections of the dashboard would be empty or hidden.

**Reporting & Correlation:** Once integrated, the platform should produce combined reports like **Marketing Overview**:

* total marketing spend (sum of all ad platforms) over a period,
* total attributable sales from marketing,
* overall marketing ROI (return on investment),
* breakdown by channel/campaign, etc.
* The platform might even suggest recommendations (like identifying the highest ROI channel or a campaign with high spend but low conversion that might need attention).

To illustrate, if a merchant uses Facebook Ads and Google Ads, the system could have a **combined ROAS report** showing: Facebook – \$X spend, \$Y revenue, ROAS Z; Google – \$A spend, \$B revenue, ROAS C; Email – \$0 direct spend (just effort) but \$D revenue etc. This gives a one-stop view rather than having to check each platform separately.

**Example (Reference):** A Facebook Ads performance dashboard might show key conversion metrics such as *Add to Cart, Checkout, Purchase events alongside ad spend to measure ROAS*. Our system will incorporate similar metrics but across channels. A multi-channel marketing funnel example (like Coupler’s Shopify marketing funnel template) uses data from Shopify, GA4, and ad platforms to visualize how impressions and clicks translate to users and then customers, including metrics like acquisition costs and ROI. The system will deliver such cross-platform funnel visualization out-of-the-box.

### **2.4 Web Analytics and User Behavior Tracking**

Understanding user behavior on the storefront (the Shopify site) is crucial to improving conversion. The system shall include **web analytics capabilities** to monitor how visitors use the site, where they come from, and what their journey is before purchasing (or before dropping off).

There are two possible approaches here:

1. **Integrate with an existing web analytics tool** (like Google Analytics or Shopify’s built-in analytics).
2. **Provide built-in tracking** via a snippet.

Shopify itself offers some analytics on traffic and behavior (for example, it can show online store sessions by source, by location, by device). Our system should either ingest that data via Shopify’s API or calculate similar metrics via our own tracking.

**User Behavior Metrics to Track:**

* **Page Views & Sessions:** The system shall record each page visit on the storefront, grouping them into sessions (a session is typically a continuous period of activity by a user). It should track number of sessions, unique visitors/users, and pageviews per page.
* **Traffic Sources:** For each session (or user), capture the referral source/medium (e.g., Organic Search, Direct, Referral, Email, Social). This can be done by parsing UTM parameters or the HTTP referrer of the first page hit in a session. The system will then be able to report **sessions by traffic source** and identify which channels bring in the most visitors. This ties into attribution for conversions as well.
* **Device & Browser:** Track device type (mobile/desktop/tablet), browser, and possibly operating system for each session. This allows metrics like “Sessions by device type” to see if mobile users behave differently (e.g., lower conversion on mobile might suggest mobile UX issues).
* **Geography:** Track the geo-location of visitors (country, region) based on IP or Shopify’s data. Show **sessions or sales by location** to identify top customer geographies. This is useful for decision-making (inventory, marketing focus, localization needs).
* **On-site Behavior Flow:** The system should capture typical click paths or funnels:

  * e.g., how many visitors view a product page → how many add to cart → how many proceed to checkout → how many complete purchase. This is essentially the funnel conversion already mentioned, but here we ensure we have the data to compute it. Shopify analytics provides “Online store conversion funnel” which includes metrics: `Added to cart`, `Reached checkout`, `Sessions converted` (with percentages) – our system will replicate and enhance that funnel.
  * If possible, capture **in-page events** like clicking “Add to Cart” (if not captured via Shopify, a tracking script can log this).
* **Bounce Rate:** The percentage of sessions that leave after viewing only one page. This indicates content effectiveness. High bounce on a landing page may signal it’s not relevant to visitors or slow to load.
* **Time on Site & Page**: Average session duration and average time on page. Useful for engagement analysis.
* **New vs Returning Visitors:** Track how many sessions are from first-time visitors vs those who have been to the site before (cookie-based or user login based).
* **Cart Abandonment Detail:** If possible, track specific cart events and contents for abandonment analysis. For example, capture what items were in abandoned carts (this can help identify if certain products are frequently abandoned).
* **Site Search Analytics:** (If the store has a search function and we can get the queries) – not a primary requirement, but could be an extra: track what keywords users search on the site and whether they result in purchases.

To achieve these, the system will likely use a **JavaScript tracking snippet** that the merchant can install on their Shopify store (e.g., by adding to the theme or via a small Shopify App script tag). This snippet would send data to our servers about page loads and events. Alternatively, since the system is a Shopify App, it can inject a script via the ScriptTag API when installed.

**Requirement F-9:** *The system shall track web user behavior either by integrating with Shopify/GA analytics or via a first-party tracking script, enabling calculation of web analytics metrics (traffic sources, user behavior, funnel steps, etc.).* This tracking must respect privacy (not gather personal info without consent – see GDPR compliance in Section 3).

**Real-Time Monitoring:** Ideally, the system could even show a real-time view of active visitors or recent activity (like “X users on site now, which pages, and if any are in checkout”). This is a nice-to-have, not a strict requirement, but modern analytics often include it. We can state: *The system should support real-time or near-real-time user monitoring for the dashboard (e.g., show active session count and live updates of sales), subject to performance considerations.*

**Behavior Analytics Outputs:** The data collected should feed into:

* **Visualization of traffic over time** (line chart of visits per day, etc.).
* **Pie charts or tables for source, device, geo distribution** (like Shopify’s dashboards).
* **Conversion funnel chart**: e.g., a funnel diagram showing drop-off at each stage (like the “Sales Funnel” in Figure 1, which shows sessions, carts, orders with percentages).
* Possibly **heatmaps or clickmaps** (not explicitly required, and likely out of scope for initial version, but something to note as an extension – e.g., integrating with a tool like Hotjar could be considered or simply not included initially).

**Requirement F-10:** *The system shall correlate web analytics with e-commerce outcomes.* For example, if the bounce rate suddenly spikes at the same time conversion drops, it may indicate a site issue – the system should highlight this (maybe via an alert or at least by allowing the user to see these trends overlaid). Another example: show conversion rate segmented by traffic source (perhaps paid traffic converts at 5% while organic at 1%, etc.). This helps in understanding quality of traffic.

**Behavioral Segmentation:** The system could allow filtering metrics by user segments (like new vs returning, mobile vs desktop, by country, etc.). E.g., “show me conversion funnel for mobile users in USA only” – to identify specific problem segments. This is an advanced capability; at minimum, providing separate metrics by segment is required (like conversion rate for mobile vs desktop as separate numbers).

**Integration with Shopify User Data:** Shopify provides some web analytics in its API (the “Analytics” API is somewhat limited, but we can get things like session referrers for orders). If needed, we could rely on Google Analytics data import for all this, but a custom solution gives us more control and avoids GA limitations (like sampled data or user needing to have GA set up correctly). We will likely implement our own tracking to ensure data completeness.

**Privacy Note:** Because tracking user behavior involves cookies or similar, we will ensure compliance with GDPR/ePrivacy by allowing opt-out and not collecting personal identifiable info without consent (discussed in Section 3 Security/Privacy). For instance, the tracking script might not activate until the user consents to analytics cookies if the merchant enables a cookie consent banner.

### **2.5 Dashboard and Reporting Features**

While UI/UX section (Section 4) will detail design, here we outline the functional capabilities of dashboards and reports delivered by the system:

* **Pre-Built Dashboards:** Upon connecting data sources (Shopify, marketing integrations), the system shall provide a set of default dashboards that cover the main use cases:

  * **Executive Summary Dashboard:** A high-level view of key metrics (total sales, conversion rate, AOV, etc. for a chosen period) and trends. Possibly includes KPI summary cards and a few trend charts.
  * **Sales Performance Dashboard:** Detailed sales metrics including breakdown by product, channel, geography, and time (sales over time chart, top products table, sales by country map, etc.).
  * **Conversion Funnel Dashboard:** Visualizes the funnel from traffic to orders, highlighting drop-off points (visitors → add to cart → checkout → purchase, with rates).
  * **Marketing Performance Dashboard:** Combining data from ads and emails as described, showing spend vs revenue, ROAS, and top-performing campaigns.
  * **Customer Analytics Dashboard:** Focused on customer metrics like new vs returning customers, CLV distribution, cohort analysis (e.g., customers acquired in a given month and their repeat purchase rate over time), and potentially an RFM (Recency, Frequency, Monetary) segmentation.
  * **Inventory/Products Dashboard:** If applicable, showing product performance, inventory status, return rates per product, etc.

  These dashboards should be readily available so the user sees value immediately. They should also be customizable.

* **Dashboard Customization:** The system shall allow users to customize dashboards or create new ones from a library of widgets. For example, a user could add a widget for a specific KPI or a chart, change the visualization type, or create a filtered view (maybe a dashboard that only shows metrics for a particular segment). At minimum, rearranging and selecting from provided widgets is expected; advanced systems allow building from scratch.

  *Requirement F-11:* *Users (with appropriate permissions) shall be able to customize the dashboards: add/remove metrics, choose chart types (line, bar, pie, funnel, table), apply filters (like date or channel filters), and save personalized dashboard views.* This way, an analyst could create a “Mobile Performance” dashboard focusing on mobile traffic metrics, for instance.

* **Interactivity:** Dashboards should have interactive elements:

  * **Date Picker** to change the period of analysis (with presets like Today, Yesterday, Last 7 days, MTD, Last Month, YTD, custom range).
  * **Filters/Segments**: filter by channel, device, location, etc., via drop-downs or tabs.
  * **Drill-down**: clicking on a data point should allow drilling deeper. For example, clicking on a “Total Sales” figure could navigate to a detailed sales report or break it down by day or by product. Or clicking on “Abandoned Carts: 61.4%” (as in Figure 1) could show a list of those abandoned cart sessions or the trend over time.
  * **Tooltips** on charts to show exact values when hovering.
  * Possibly **cross-filtering**: e.g., clicking on a segment in a pie chart (like “Mobile” in revenue by device) filters the entire dashboard to mobile users.

* **Standard Reports:** Besides dashboards, the system should offer more detailed reports, often in tabular form, possibly with pagination and the ability to export (this ties to Data Export in Section 7). For example:

  * **Sales Report** (detailed list of orders with columns and filters),
  * **Product Report** (sales by product),
  * **Customer Report** (customer list with CLV, last purchase date, etc.),
  * **Marketing Report** (campaign level data).
    Many of these might simply be accessible by drilling down from dashboards, but listing them explicitly as features ensures they are considered.

  *Requirement F-12:* *The system shall provide detailed tabular reports for key entities (orders, products, customers, campaigns), with the ability to sort, filter, and search within those reports.* For instance, a user could filter the Orders report to show all orders coming from the “Email” channel in last month with value > \$100. Or filter the Products report to show only a certain collection.

* **Multi-Store Support:** Some users (agencies or owners of multiple Shopify stores) might connect more than one store to the platform. The system should handle multiple data sources separately and possibly in aggregate:

  * If a user has 3 Shopify stores, they might want to either view analytics per store or an aggregated view. In Figure 1, “Ashley – 3 stores selected” indicates a selection of multiple stores to aggregate.
  * Our requirement: *The system shall support multiple store connections under one account and allow the user to toggle between stores or view combined analytics.* Combined view is advanced (requires merging data, ensuring no overlap in customers unless desired), but at least toggling one store at a time is necessary. This is particularly useful for agencies or consultants. (This touches on multi-tenant handling in architecture, as each store is essentially a tenant whose data must be isolated but can be aggregated for an authorized user – see Security and Roles for ensuring only the right people see each store’s data).

* **Internationalization in Data:** If the store sells in multiple currencies (Shopify stores can have multi-currency), the system should handle currency conversion or separate metrics per currency. Ideally, all financial metrics should be shown in the store’s primary currency by default. If multiple currencies are used, either convert them to a single currency using exchange rates or allow filtering by currency. *Requirement:* *The system shall handle multi-currency data by either consolidating values in a base currency (with clear indication and conversion rates used) or by allowing the user to view metrics per currency.* (We might rely on Shopify’s converted totals if available through API to simplify this).

* **Forecasting (Future Feature):** Not explicitly required in prompt, but analytics systems often add forecasting or predictive insights (e.g., projecting sales for next month, predicting customer lifetime). While not a current requirement, the design should not preclude adding such features later (extensibility). For completeness, we note that *in future, the system may incorporate predictive analytics like forecasting sales or predicting churn, using the collected data.* (Non-functional extensibility will cover this.)

This concludes the functional requirements. In summary, the system provides rich analytic functions: tracking a wide array of KPIs, merging data from multiple channels, tying in marketing campaign data, analyzing on-site user behavior, and presenting everything in customizable, interactive dashboards and reports. All functional features will be implemented with a focus on accuracy, security, and usability as detailed in the following sections.

## **3. Non-Functional Requirements**

Non-functional requirements define the qualities and constraints of the system – how it operates rather than specific features. This includes performance, security, scalability, and compliance needs that are crucial for a robust SaaS product.

### **3.1 Performance and Scalability**

**Performance Targets:** The system must perform efficiently for end-users, ensuring that dashboard queries and page loads are fast, even as data volume grows.

* **Dashboard Load Time:** Dashboards (especially the main summary) should load within **3 seconds** for typical data volumes (for a small-to-medium merchant) and ideally under 5-7 seconds even for large datasets. Interactions like applying a filter or changing date range should update visualizations within 2-3 seconds. If data needs to be pre-aggregated to achieve this, that’s part of the technical design.
* **Data Freshness:** Newly incoming data (e.g., a new order on Shopify, or new ad data) should reflect on the dashboard quickly. **Real-time goal:** within 1-2 minutes of an order happening, the KPI values update (since Shopify webhooks can push data instantly – see Technical integration). Ad data might be near-real-time (within 1 hour for example). The requirement is to have intraday updates rather than only next-day.
* **Throughput:** The backend should handle a high volume of events if needed. For instance, if tracking web analytics, a busy Shopify store might generate many events (page views, etc.). The system should handle at least **hundreds of events per second** ingestion without losing data for larger clients. For smaller typical clients, this ensures plenty of headroom.
* **Concurrent Users:** The platform should support many users viewing dashboards simultaneously, across all customers. As a multi-tenant SaaS, it might have hundreds or thousands of merchant users logged in during peak hours. The infrastructure must support, say, **1000 concurrent active users** with no degradation in response time beyond acceptable limits.
* **Bulk Data Processing:** Operations like initial data import (when connecting a Shopify store with possibly years of history) or generating a large report (e.g., export all orders of last year) should be handled in a time-efficient manner. For example, initial sync of 100k orders should complete within a few hours at most (preferably quicker), employing background processing so the user can be notified when ready rather than blocking them.
* **API Performance:** If the system exposes APIs (for data export or integration), those should respond within typical REST guidelines. Queries for specific data should be optimized (e.g., retrieving a small range of data in < 1 second; bulk data via paginated endpoints streaming as quickly as possible).

**Scalability:** The system should scale both **vertically** (handle increasing data volume per customer) and **horizontally** (handle increasing number of customers).

* **Data Volume Scale:** Design for supporting large Shopify merchants (e.g., ones with millions of orders and customers). The data pipeline and storage should be able to manage **tens of millions of records** (orders, events) without significant slow-down, by using appropriate technologies (like a columnar database for analytics, proper indexing, archiving old data if needed, etc.). The analytics queries should use pre-computed aggregates or caching for big data sets to keep response times manageable.
* **User Base Scale:** The architecture must allow adding more servers or resources to accommodate more tenants. For example, if 100 new shops sign up per week, the system should handle that growth by scaling out web servers, job processors, and databases as needed. We target being able to serve **thousands of Shopify stores** on the platform, from small shops to enterprise Shopify Plus clients.
* **Multi-Tenancy Efficiency:** The design should reuse resources among tenants where possible but also isolate heavy workloads. For instance, an expensive query for one tenant should not monopolize shared resources and starve others (using query timeouts or separate query pools, etc.). We may employ multi-tenant aware caching — e.g., common queries (like industry benchmarks) could be cached globally, and tenant-specific queries cached per tenant.

**Availability & Reliability:** (though often separate, we include here as it relates to performance in terms of uptime)

* The system should be highly available, ideally **99.9% uptime or higher** (which equates to < \~45 minutes downtime per month). This means employing redundant servers, failover mechanisms, and avoiding single points of failure (see next section).
* In the event of downtime or maintenance, read-only fallback could be considered (e.g., dashboards show last available data with a notice instead of being completely unavailable).
* System should handle network or API failures gracefully: e.g., if Shopify API is temporarily down or rate-limited, our system should retry later and notify users if data is temporarily stale.
* Data integrity is part of reliability: the system should avoid data loss. All imported data should be stored safely (with backups, see Data storage section).

### **3.2 Availability, Reliability, and Scalability Architecture**

*(Combining availability with scalability to cover system architecture aspects.)*

**System Architecture for High Availability:** The system will be built on a cloud-based architecture with redundancy:

* **Web/App Servers:** Deployed in a load-balanced cluster. At least two instances in production such that if one fails, others continue serving requests. Can scale out with more instances during high load.
* **Database:** Use a managed highly-available database (e.g., a cluster with primary and replicas, or a distributed database). Employ automated backups and possibly point-in-time recovery for the database to prevent data loss.
* **Data Processing:** If using background workers (for data ingestion, metric computation), there should be multiple workers so that if one fails others pick up tasks. Possibly use a messaging/queue system (like AWS SQS, RabbitMQ, or Kafka) to decouple ingestion and processing, which naturally supports reliability by storing tasks until done.
* **Geo-Redundancy:** If serving a global user base, consider deploying in multiple regions (e.g., US and EU) to reduce latency and for redundancy in case one region has issues. However, ensure data residency compliance (e.g., EU customers’ data stays in EU if required by GDPR – see Security).
* **Graceful Degradation:** In case of partial outages (say marketing API is down), the system should still serve other data and clearly mark the sections that are unavailable (“Facebook Ads data is currently unavailable; last update X hours ago”). This avoids a complete failure of dashboards if one component fails.

**Scalability Strategies:**

* Design using microservices or modular components: e.g., separate the web frontend, the data ingestion service, and the analytics computation engine so they can scale independently. For instance, if tracking heavy web events (analytics), have a dedicated service ingest and summarize those, so the main app isn’t overloaded.
* Use of cloud auto-scaling for stateless parts (web servers, workers).
* Partitioning of data if needed: For very large datasets, consider partitioning the analytics data by date (like by month or year) to keep queryable chunks reasonably sized.
* Caching layer: Employ caching (like Redis or in-memory caches) for frequently accessed data, especially expensive queries or common aggregates. For example, cache the daily sales totals for the last 30 days and update when new orders come in, rather than re-querying the entire order table each time.
* As data grows, we may move older data to cheaper storage (data archiving) but ensure it’s still accessible for historical reports (maybe with slightly longer query time or on-demand retrieval).

**Load and Stress Testing:** The system will be tested under heavy load scenarios to verify these non-functional requirements. For example, simulate 1000 concurrent users querying a year of data to ensure the system remains responsive or degrades acceptably. The design will incorporate results from such tests (like adding indexes if queries slow down beyond target, or increasing resources where needed).

### **3.3 Security Requirements (including Privacy & GDPR)**

Security is paramount as the system deals with sensitive business data (sales figures, customer personal data) and integrates with multiple external accounts. Security requirements include data protection, access control, and regulatory compliance (GDPR and others).

**Authentication & Access Control:**

* The system shall enforce secure authentication for users. This likely includes **username/password** login for the SaaS account, with password hashing stored (never plain text). We should use strong password policies (minimum length, encourage mix of characters) and possibly offer 2-Factor Authentication (2FA) for added security.
* Since many users will sign up via Shopify (likely this analytics system could be a Shopify App), consider implementing **OAuth with Shopify** for initial sign-in. For example, when a merchant installs the app via Shopify, we receive a token and create an account linked to their Shopify store. They might then access our app’s dashboard via single sign-on from Shopify’s admin. Regardless, any direct login should be protected.
* All communications will happen over HTTPS (TLS 1.2+). **Encryption in transit** is mandatory: API calls between our system and Shopify or others must use HTTPS, and our web app served via HTTPS to users.
* **Session Security:** Use secure cookies for sessions, with HttpOnly and Secure flags, proper session timeout, and possibly IP or device checks to mitigate hijacking.
* **Authorization (Roles):** Implement the role-based permissions as per Section 5. Ensure that a user from one merchant (tenant) cannot access data from another. This is critical in a multi-tenant environment: data queries must always be scoped to the user’s store/organization. Proper checks on every API endpoint and query will enforce tenant isolation.
* **API Security:** When connecting to Shopify and other APIs, use OAuth tokens or API keys securely. Do not expose these to the front-end. Store them encrypted in our database. Use the principle of least privilege – request only the scopes needed (e.g., if we only need read access to orders and analytics from Shopify, do not request write scopes or other data we don’t use). Same with other integrations (e.g., only read ad data, not manage ads).
* Protect our own APIs against misuse: rate limit if needed to prevent DDoS or accidental overload (especially if we provide open API to users to query data).

**Data Security & Encryption:**

* **Encryption at Rest:** All sensitive data in the database should be encrypted at rest. If using a managed DB, ensure disk encryption is enabled. Additionally, consider application-level encryption for highly sensitive fields (like customer personal info) – though that can complicate analytics, so perhaps rely on database encryption and strict access control.
* **Backups:** Ensure backup files are also encrypted. Backup retention policies should be defined (e.g., keep daily backups for X days, weekly for Y weeks, etc.) and stored securely.
* **Least Privilege:** Only authorized system components and personnel can access production data. For example, developers should not have direct access to live customer data except through secure mechanisms. This might be outside scope of SRS, but it’s good to note adherence to security best practices like SOC 2 guidelines if aiming for that certification in future.
* **Secure Development:** The software will be developed following secure coding practices to avoid common vulnerabilities (SQL injection, XSS, CSRF, etc.). For instance, use prepared statements for DB queries, output encoding for any dynamic content in UI, and CSRF tokens for form submissions. Regular security testing (penetration testing, code analysis) will be performed.

**GDPR Compliance:** Given that merchants may have customers from the EU, GDPR applies to any personal data processed (e.g. customer data from Shopify includes names, emails, addresses – that’s personal data; also tracking user behavior sets cookies – also personal data or at least online identifiers).

Key GDPR principles to comply with:

* **Lawful Basis & Consent:** The system is processing data on behalf of merchants (who are controllers, we are a processor in GDPR terms). We need a Data Processing Agreement with merchants likely. For tracking website visitors, the merchant should obtain consent via cookie banner for analytics if required by law. Our system should provide tools to respect those consents (e.g., the tracking script won’t start tracking until consent given if merchant flags it).

* **Data Minimization:** Only collect data that is necessary for the analytics purposes. For example, we don’t need to store a customer’s full credit card or even full address for analytics – we might only need country or city at most. So, avoid pulling unnecessary PII from Shopify. Perhaps focus on order and product data, and basic customer info (maybe name/email for customer-level tracking like CLV, but even email could be hashed if not needed in reports).

* **Anonymization/Pseudonymization:** When feasible, personal identifiers in our analytics data should be pseudonymized. For instance, for web tracking, we might assign a unique user ID but not store their real identity unless they log in. If we store any personal data (like customer email to join with email campaign data), consider hashing it for internal linking so that if our DB is compromised, raw emails are not exposed.

* **Right to Access & Portability:** Provide means to export all personal data we have about individuals if requested (likely through the merchant). For example, if a customer asks the merchant for their data (GDPR data access request), the merchant can use our system’s reports to retrieve all info on that customer (orders, etc.). We could implement a search by email or customer ID and output all related analytics data. Also ensure any data we have that came from Shopify can be tied back to the customer so it can be retrieved or deleted.

* **Right to Erasure:** This is critical with Shopify’s requirements. Shopify mandates apps to handle GDPR webhooks: **customers/redact** and **shop/redact**. Specifically:

  * When a store owner requests deletion of a customer’s data or a customer requests it, Shopify will send `customers/redact` webhook to our app with customer ID, and we must delete all personal data for that customer in our system.
  * When a store uninstalls our app (or after 48 hours of uninstall), Shopify sends `shop/redact` webhook, and we must delete all personal data from that store.

  *Requirement N-1 (GDPR Delete):* *The system must implement Shopify’s GDPR mandatory webhooks for data erasure.* Upon receiving `customers/redact`, delete or anonymize the customer’s data in our database (e.g., remove their name, email, replace with a generic identifier in orders, etc.). Upon `shop/redact`, purge all personal data (customer info) for that store and any store-specific data as required. (We may keep non-personal aggregate stats in a generic form, but likely easier to delete everything for compliance.)

  Additionally, Shopify provides `customers/data_request` webhook when a customer requests a data export. We should respond by collating that customer’s data and perhaps sending it to the store owner or making it available. At minimum, ensure we have a way to get all data for a given customer quickly for this purpose.

* **Consent Management:** For the tracking script, provide configuration for a cookie consent:

  * The merchant might input their cookie consent mechanism’s integration. Or we provide a snippet that respects a JavaScript global flag for consent. Essentially, ensure no cookies or tracking on EU visitors before consent.
  * If a visitor opts out (do-not-track), our script should honor that and not send further events.
  * Provide an easy way for merchants to exclude specific users from tracking (maybe internal IP filtering, etc., though that’s more a convenience feature).

* **Privacy Policy:** We will maintain a clear privacy policy (likely via the company, not part of the software itself, but mention that usage of the system implies agreement to how data is processed).

* **Data Residency:** If needed, allow EU customer data to be stored in EU data centers. Depending on infrastructure, we might choose a region accordingly or have separate instances. While not explicitly demanded, some enterprise clients might require it. Our system should be able to be configured for region-specific data hosting if the business model supports that.

**Auditing and Logging:**

* Log important actions: admin logins, configuration changes, data exports, etc., for audit trail.
* Log accesses to data maybe at an aggregate level (not each view, that’s too much, but any time an admin queries a particular customer’s data outside normal aggregate? Possibly unnecessary).
* Monitor for unusual patterns (like someone pulling data of all customers frequently might indicate a misuse or breach).

**External Integrations Security:**

* Tokens from marketing integrations should be stored securely and refreshed as needed. If a token is compromised or an integration is removed by the user, ensure to revoke it properly.
* Ensure our usage of third-party APIs complies with their policies (to avoid our app getting blocked for too many requests or misuse).
* **Rate limiting:** Respect Shopify API rate limits (they allow a certain number of requests per second). Use efficient GraphQL queries when possible to reduce number of calls. For webhooks, ensure our endpoint is performant to handle bursts (Shopify might resend if we don’t respond 200 quickly).

**Penetration Testing & Vulnerability Management:**

* Regularly perform security testing (or have a bounty program or at least internal audits).
* Keep dependencies updated to patch known vulnerabilities.

By adhering to the above, the system will safeguard merchant data and customer privacy, building trust with users which is essential for an analytics product.

### **3.4 Compliance and Other Non-Functional Requirements**

Beyond GDPR, mention of **CCPA** (California Consumer Privacy Act) should be considered. Similar to GDPR, giving California residents rights to access/delete data. Our policies to handle deletion requests and data exports cover this largely. We’ll ensure our privacy features meet CCPA and similar laws (like Canada’s PIPEDA, etc.) by extension.

**Usability & Accessibility:** (Though more UI, but a non-functional aspect)

* The application should be easy to learn for non-technical users (store owners, marketers). Use of clear language, helpful tooltips (especially explaining analytics terms) is required. We should avoid excessive jargon or at least define it (like we do for KPIs).
* **Accessibility (a11y):** Strive to meet **WCAG 2.1 AA** guidelines so that the dashboards are usable by people with disabilities. This includes: proper semantic HTML for screen readers, sufficient color contrasts in charts and text, ability to navigate via keyboard, and providing text alternatives for non-text content (like charts should have summaries or data tables accessible).
* **Responsive Design:** The UI should be responsive to different screen sizes. Many users might check stats on a tablet or phone. While complex dashboards are hard to fully show on mobile, at minimum a simplified responsive view (perhaps key metrics and ability to scroll charts) should be available. So performance on mobile browsers and layout adjustments for small screens is expected.

**Maintainability & Extensibility:**

* The system should be built in a modular way to allow adding new data connectors (e.g., another ad platform) or new metrics without a complete rewrite. For example, if a new KPI is requested, developers should easily plug it into the data model and UI.
* Code should be documented, and configuration (like API keys, endpoints) externalized so updates can be made without code changes when possible.
* The platform should be designed for updates with zero or minimal downtime (using techniques like rolling deployments).

**Scalability of Organization:** If many user accounts exist under one organization (like an admin invites multiple analysts, etc.), the system should handle that (this ties into Roles & Permissions and is a functional point as well). But from a performance view, having 50 users simultaneously working in one account with many custom dashboards should not degrade the system – implies efficient handling of user-specific settings.

**Support & Monitoring:**

* There should be application monitoring in place (APM) to track performance metrics of the system itself (response times, error rates) so the devops team can proactively address any issues (this is internal but ensures we meet performance SLAs).
* The system should provide meaningful error messages if something goes wrong (e.g., “Data for XYZ is temporarily unavailable. Please try again later.” rather than just generic failure). Also possibly an in-app status page if some integrations are failing.
* Have a plan for **disaster recovery:** if a major failure happens (e.g., data center outage), we can restore service from backups in another region within a certain RTO/RPO (Recovery Time/Objectives), say RTO of a few hours and RPO of at most an hour (meaning we might lose at most one hour of data in worst case, which is acceptable for analytics – though with proper design, even that can be minimized).

In summary, the non-functional requirements ensure the analytics platform is **fast, scalable, secure, highly available, and compliant with privacy laws**. These qualities are crucial to handle the potentially sensitive and high-volume data involved in e-commerce analytics while providing a reliable service to all users.

## **4. UI/UX Requirements**

User Interface and User Experience requirements focus on how the system will look and behave for the end user. This section describes the design principles, interface components, and behaviors that will ensure the product is intuitive, visually clear, and effective in conveying information to Shopify users. It also covers support for multiple languages and other UX considerations.

### **4.1 General Design & Usability**

* **Clean, Intuitive Layout:** The UI should use a clean dashboard-style layout with clear separation of sections (navigation menu, header with filters, content area for charts/tables). It should adopt a modern flat design with Shopify-like aesthetics (so it feels integrated). Key information (KPIs) should be prominently displayed in cards or at the top of the dashboard for quick scanning.
* **Consistency:** All pages should follow a consistent style guide – colors, typography, and component styles should be uniform. Use Shopify Polaris design system for inspiration or integration if possible (Shopify’s app design guidelines) to match the look-and-feel that Shopify merchants are used to.
* **Navigation:** Provide a sidebar or top navigation menu with clear labels for each main section or dashboard (e.g., “Overview”, “Sales”, “Customers”, “Marketing”, “Settings”). Icons can accompany text for quick recognition. Breadcrumbs can be used when drilling into detailed pages to allow easy back navigation.
* **Short, Informative Content:** Avoid long paragraphs in the UI; information should be presented concisely via charts, labeled metrics, or tooltips. If explanation is needed (for a metric or feature), use tooltips or help modals so the UI remains uncluttered. As per user’s preference, paragraphs (if any in UI like descriptions) should be short and to the point (3-5 sentences max as a guideline for any help text).
* **Responsive Behavior:** As noted, the layout should adapt to different screen sizes. On large screens, multiple charts can be side by side; on mobile, they may stack vertically. Use a hamburger menu for navigation on mobile, and ensure charts are scrollable if they overflow. Important KPIs should still be visible without excessive scrolling on a small screen (maybe an overview list).
* **Interactive Elements Clarity:** Buttons, filters, and other interactive controls should be clearly indicated (distinctive styling, hover effects). E.g., date filter dropdown should be obvious as a clickable element. Use loading spinners or skeleton screens to indicate when data is being loaded after an interaction, so user knows the system is working.
* **Help & Onboarding:** For first-time users, possibly provide a quick onboarding tour highlighting key areas of the dashboard (“This is your conversion rate – it shows...”). Also have a help center or documentation accessible (maybe a “?” icon or link to a user guide).
* **Error Handling in UI:** If something fails (like an API connection), show user-friendly error messages with guidance. E.g., “Failed to fetch Google Ads data. Please check your connection in settings or try again later.” If a chart has no data (e.g., no campaigns), display a message “No data available” rather than a blank space.
* **Color and Visual Encoding:** Use color coding meaningfully but sparingly:

  * Perhaps green for positive trends (upward arrow next to metrics that increased), red for negative (down arrow on a dropping KPI).
  * Use a distinct palette for different chart series (e.g., each channel has a color consistently across charts).
  * Ensure colors have enough contrast (especially for text and important lines) to be readable (accessibility requirement).
  * If color indicates something like above/below target, also use an icon or text so that colorblind users can interpret (don’t rely solely on color).
* **Fonts and Text:** Use a clean sans-serif font (likely whatever Shopify apps default to, or something like “Helvetica/Arial or Shopify’s system font”). Important numbers can be slightly larger or bold. Support formatting numbers with commas, currency symbols, etc., correctly per locale. Dates should appear in a user-friendly format (e.g., “Jan 15, 2025” or according to user’s locale preference).

### **4.2 Dashboard UI Details**

Each dashboard (as described in functional requirements) will consist of various **widgets** (charts, tables, metric cards). The UI requirements for these components are:

* **KPI Summary Cards:** At the top of an overview dashboard, have several cards displaying key metrics (like Total Sales, Conversion Rate, AOV, etc. for the selected period). Each card will show:

  * The metric name (e.g., “Total Sales”).
  * The value (e.g., “\$147,395” as in Figure 1’s pie chart center or as a card).
  * Possibly a comparison to previous period (like a small label or arrow saying “+5% vs last month”).
  * Maybe an icon or small chart sparkline for trend.
  * These cards should be easily glanceable. They might be laid out in a grid (responsive to columns on big screen, single column on small).

* **Charts:** Common chart types to implement: line charts, bar charts, stacked bar or area charts, pie/donut charts, funnel diagrams, tables.

  * **Line/Area Charts:** for trends over time (e.g., daily sales). Should have axes labeled (time on X axis, value on Y). Allow toggling series if multiple series (like show/hide net profit line).
  * **Bar Charts:** e.g., revenue by channel (a vertical bar for each channel, or horizontal bar with values labeled). If values differ greatly, consider log scale or break axis if needed, though usually just straightforward.
  * **Stacked Bar/Area:** e.g., stacked area for cumulative contributions (in Figure 1, bottom middle chart looks like a stacked area of sessions by source over time). That helps visualize composition.
  * **Pie/Donut Charts:** e.g., % breakdown of channel or device or country (like “Revenue by Device” in Figure 1 is a pie). Ensure labels or legend identifies slices clearly (with percentage and category).
  * **Funnel Chart:** Represent the e-commerce funnel. Could be a stylized funnel graphic (wide to narrow) with labels at each section showing absolute numbers and percentages of starting figure. E.g., Sessions: 92,876; Added to Cart: 10,923 (11.8% of sessions); Orders: 4,219 (4.5% of sessions). This is depicted in Figure 1 (Sales Funnel).
  * **Tables:** Used for detailed data like lists of top products or customers. Should be sortable by columns, allow search. Only show maybe 5-10 rows by default with option to expand or go to full report page.

* **UI Behavior for Filters:**

  * **Date Range Picker:** A control (maybe top-right of dashboard, as seen “Jul 1, 2018 – Jul 31, 2018” in Figure 1 example). Clicking it opens a calendar to choose range or presets (Last 30 days, etc.). When changed, all widgets update to that range. If the user picks a very long range and data volume is huge, perhaps show a warning or aggregate by week/month to maintain performance (or just ensure backend handles it).
  * **Channel/Segment Filters:** Could be multi-select dropdowns or pills. For instance, a filter for “Channel” with checkboxes for each channel (Shopify, Amazon, etc.) – if user selects only Amazon, all charts filter to Amazon orders/traffic. Similarly, a filter for “Device: All/Mobile/Desktop” or “Customer Type: All/New/Returning”. These filters, if multiple, could appear as a filter bar. They should apply instantly or with an “Apply” button if multiple selections.
  * If too many filters would clutter UI, possibly a sidebar filter panel or a top bar that reveals more filters on click (like a funnel icon to open filter menu).

* **Interactive Drill-Down:** For UX:

  * If a KPI card is clicked, navigate to a relevant detailed view. E.g., clicking “Conversion Rate” might open a page or modal with breakdown by traffic source or a trend over time for conversion.
  * If a section of a chart is clicked (like a bar for “Email” in revenue by channel), perhaps filter the dashboard to that channel (as mentioned) or show details (maybe a tooltip with more info or trigger a filter).
  * Provide clear affordances for clickable elements: e.g., make the card highlight on hover or show a “View details” icon.

* **Annotations & Explanations:** The UI might allow adding notes or annotations. Not a must-have, but if a spike happened and user wants to note “Launched campaign X here”, an annotation on a chart could be useful. At minimum, the system itself could show annotations for known events if data available (like “Promotion period”).

* **Multi-Language Toggle:** If internationalization is supported (see 4.4), allow user to pick language in settings or auto-detect.

* **Dark Mode:** Not required but a plus if many users work at night or prefer it. Could be considered (with proper chart color adjustments).

### **4.3 Example User Interface Scenarios**

To illustrate some UI/UX requirements, consider the following usage scenario:

**Scenario:** A merchant logs in on Monday morning to see how the weekend performed.

* They are greeted with the **Overview Dashboard** (Main Dashboard). At a glance, they see:

  * A row of KPI cards: *Total Sales*, *Conversion Rate*, *Avg Order Value*, *New Customers*, *Cart Abandonment* for the last 7 days.
  * Each card possibly has a small indicator: e.g., “\$50,000 Total Sales (+10% vs prior week)”, “2.5% Conversion Rate (▼0.2%)” with a red down arrow indicating it dropped a bit.
  * Below, a couple of charts: a line chart of daily sales for the last 7 days, maybe a bar chart of sales by channel over that period, and a funnel graphic for conversion.
* The merchant wants more detail, so they click on the “Sales Performance” section.

  * This might be a separate tab or page. It shows perhaps a larger chart of sales over time with ability to switch between daily/weekly view, a table of orders or summary by day.
  * They see a **Revenue by Country** map or table (like in Figure 1 bottom left, showing US etc.).
  * They can toggle a dropdown to see “Last 30 days” instead. The charts update accordingly.
* They then check the “Marketing” dashboard to see how their Facebook and Email campaigns did.

  * On the Marketing dashboard, there’s a panel for Facebook Ads: a chart for *Spend vs Revenue vs ROAS over time*, and below it key metrics (Total Spend, Impressions, Clicks, Conversions).
  * There’s another panel for Email: showing *Open Rate, CTR, Revenue from Emails* for the last campaign sent.
  * If they see one campaign underperformed, they might click it to go to a “Campaign Details” page (a table listing each campaign).
* Next, they go to “Customers” dashboard to see new customers and CLV trends.

  * There’s a cohort analysis chart or table (e.g., customers acquired each month and their repeat purchases in subsequent months).
  * A list of top customers by sales might be shown.
* In all these, the UI allowed them to get info quickly with minimal clicks, and any deeper data is a click away but not forced if they just want high-level.
* They notice something odd: a low conversion rate on mobile devices. They use a filter toggle for Device = Mobile on the funnel chart. It updates to show that indeed mobile conversion funnel drops heavily at checkout. This insight might prompt them to investigate their mobile checkout UX or test it.
* Finally, the user goes to the “Settings” or “Integrations” page via the nav menu to perhaps add a new integration or invite a colleague.

  * The Settings page UI will list connected accounts (Shopify – connected, Google Ads – connected, etc., maybe with green indicators; and an option to connect more).
  * There’s also a “User Management” section (for admins) to invite users and assign roles – a simple form interface.

Throughout, the UI kept a consistent header (maybe with the product name and a link back to main dashboard), and maybe a profile menu at top right for account settings/logout.

### **4.4 Internationalization & Localization**

The system shall support **internationalization (i18n)** so that the UI can be translated into multiple languages and formatted for various locales.

* **Language Support:** All text in the UI (labels, headings, tooltips, error messages, etc.) should be externalized into resource files for easy translation. Initially, English will be provided. The system design should allow adding languages such as Spanish, French, German, Chinese, etc., as needed for market expansion. Users should be able to select their preferred language, or it could default based on their browser/Shopify locale.
* **Dynamic Content Translation:** Note that certain content like KPIs names might be known terms globally (some may keep in English like “AOV” acronym, but we should translate the full name). We’ll provide translated strings for all metric names and common terms (e.g., “Conversion Rate” -> “Taux de conversion” in French, etc.).
* **Number/Currency Formatting:** The UI should format numbers according to locale. For example, in European format “1,000.50” may be written “1.000,50”. Likewise, date formats should adapt (MM/DD/YYYY vs DD/MM/YYYY, etc.). Ideally use a library or framework features for locale-specific formatting. Currency should show in the correct symbol (if multi-currency, or at least the primary currency symbol of the store with proper placement e.g., “€” before or after value depending on locale).
* **Timezone:** If merchants are globally distributed, ensure that date/time displayed (like “Last updated at 5:00 PM”) is shown in the user’s local timezone or clearly labeled. If a store’s data is mainly in a certain timezone (Shopify store has a set timezone), use that consistently for reporting daily totals, etc., to avoid confusion (e.g., align with how Shopify reports daily sales).
* **Content Localization:** Even some analytics concepts can vary (or their abbreviations). We’ll consult with translators who know e-commerce to ensure translations make sense. For instance, “cart abandonment” in Spanish should be an accurate term used in e-commerce context.
* **Right-to-Left (RTL) Support:** If supporting languages like Arabic or Hebrew, the UI should accommodate RTL reading order. This means the layout might flip (charts remain left-to-right for time maybe, but text align and nav placement might change). This is an extra complexity; but at least ensure no hard assumptions that break the UI if text is longer or different direction.
* **Units and Conventions:** If any units are used (like weight in some inventory context, or date first day of week), adapt or allow customization. For example, week starting Monday vs Sunday might be a minor consideration for some calendars.

### **4.5 Wireframes / UI Examples (Description)**

*(If actual wireframe images were available, we’d include them. Lacking that, we describe them.)*

To give a clearer picture, here’s a description of a couple of screen layouts:

* **Figure 2: Overview Dashboard Wireframe (conceptual)**:

  * Header: Product Logo & Name on top-left, user profile top-right, date filter top-right.
  * Primary content: A 2-column layout (on desktop). On the left, a column of KPI summary cards (e.g., 4 cards stacked or in grid). On the right, a large line chart showing revenue over time.
  * Below, full width section: a multi-column area with, say, three charts side by side: (1) Conversion Funnel graphic, (2) Pie chart for Sales by Channel, (3) Pie chart for Sales by Device.
  * Next row: two half-width charts: (1) Bar chart or map for Sales by Country, (2) Table for Top Products.
  * Each chart has a title at top (e.g., “Revenue by Channel”) and possibly a settings icon to customize or expand.
  * The sidebar navigation is visible on left with icons+text: Dashboard (selected), Sales, Marketing, Customers, etc.

* **Figure 3: Marketing Dashboard Wireframe**:

  * Navigation indicates we are in Marketing section.
  * Top section: filters to select which channels to display (e.g., checkboxes for Facebook, Google, Email – to include/exclude their panels).
  * A grid of panels:

    * Facebook Ads panel: shows summary (Spend, ROAS, etc.) and a trend chart.
    * Google Ads panel: similar structure.
    * Email Campaigns panel: maybe a table of recent campaigns with open/click rates, and a bar chart of revenue by campaign.
  * If one panel is not connected (e.g., Google Ads not integrated), that panel could show a “Connect Google Ads to see data” with a button.
  * Each panel likely has a “View Details” link to go to a full-page report for that channel (with breakdown by campaign or ad).

* **User Management Page**:

  * A simple table of current users (Name, Email, Role) and an “Invite User” button.
  * Invite user opens a modal to enter email and select role from dropdown (Admin/Analyst/Manager).
  * Admin can change roles via a dropdown in the table or remove users.
  * This page should be straightforward and consistent with typical SaaS user management designs.

*(Since embedding actual wireframe images isn’t done here, we rely on descriptive wireframes. The actual implementation would use a frontend framework to render such components.)*

### **4.6 Accessibility & Keyboard Navigation**

Ensuring the interface is navigable and usable by all users:

* All interactive elements must be reachable via keyboard (tab order should flow logically through menus, filters, then content).
* Charts pose a challenge for screen readers; we will include descriptive text or summaries for charts. For example, an aria-label on the chart could say “Revenue by Channel: Direct 45%, Organic 29%, etc.” or provide a hidden table of the data.
* Provide skip links if needed to jump to main content (especially if navigation is long).
* Use ARIA roles properly (e.g., role “navigation” for nav bar, headings for sections, etc.).
* Testing will be done with screen reader (like NVDA/JAWS) to ensure key parts are announced meaningfully.

### **4.7 UX for Integration Setup and Errors**

When the user first sets up the product, a friendly flow should guide them:

* After installing the app or signing up, they see a **welcome screen** maybe: “Welcome to E-Com Analytics! Let’s connect your data sources.” Steps might be shown.
* Step 1: Shopify is likely already connected by the installation process (we have an API token from Shopify).
* Step 2: Prompt to connect other channels: “Connect your marketing platforms” with buttons for each. If they skip, fine – but highlight they can do it later in settings.
* After initial setup, perhaps show a loading state or “Data is being imported, this may take a few minutes.” Provide either a progress bar or at least a message that “We’re fetching your historical data from Shopify (500 orders processed out of 2000…)”. The user could explore partial data if available or wait; important is to set expectations so they don’t think it’s broken.
* If an integration (like Facebook) fails authentication or token expires, UI should clearly prompt re-authentication in Settings.
* The Settings UI should show status of each integration (Connected, Needs Reconnect, etc.). E.g., if Facebook token expired after 60 days (as they do), we mark it and have a “Reconnect” button.

### **4.8 Future UX Considerations**

As new features are added (like forecasting or ML insights), design their UI elements in line with existing style. E.g., a forecast might appear as a dashed line extending from the sales chart into the future, with a label “Projected”. Or alerts might appear as notification icons.

In conclusion, the UI/UX requirements ensure that the powerful analytics provided by the system are presented in a **user-friendly, clear, and responsive interface**. By adhering to these guidelines, even a non-technical Shopify merchant can navigate the dashboards, understand their store’s performance at a glance, and dive into details as needed, all while enjoying a polished user experience that integrates seamlessly with their daily workflow.

## **5. Technical Requirements**

This section outlines the technical aspects of the system, including architecture, integration specifics with Shopify and other APIs, how data flows through the system (data pipeline), and other implementation considerations. It effectively bridges the gap between functional needs and the actual implementation plan.

### **5.1 System Architecture Overview**

The system will follow a **modern web application architecture**, likely a three-tier (or multi-tier) design with separate components for data ingestion, processing, storage, and presentation. Below is a high-level overview of the architecture and data flow:

* **Data Sources:**

  1. **Shopify API:** Source of orders, products, customers, etc.
  2. **Marketing/Ads APIs:** Facebook Graph API, Google Ads API, Mailchimp/Klaviyo API, etc.
  3. **Web Analytics Events:** from our tracking script on the storefront (or GA API if used).
  4. Possibly other sources like CSV uploads or other integrations in future.

* **Ingestion Layer:** Responsible for pulling or receiving data from sources.

  * **Webhooks:** Shopify will send webhooks for real-time updates (order creation, update, refund, etc.). Our system exposes endpoints to receive these (e.g., `/webhook/shopify/order_created`). Also GDPR webhooks as mentioned.
  * **API Polling/Fetching:** For data that doesn’t have webhooks (e.g., pulling ad spend from Facebook), scheduled jobs will call those APIs periodically (e.g., every hour or daily).
  * **Tracking Script Events:** Received via an endpoint (e.g., client-side script sends a POST to `/collect` on our server for each page view or event).
  * This layer may use a **message queue** to buffer and distribute tasks. For example, a webhook triggers a job added to queue “process\_new\_order” to be handled asynchronously so the webhook response is quick.

* **Data Processing Layer:** Where raw data is transformed, aggregated, or stored.

  * Could be broken into subcomponents:

    * **ETL Jobs:** e.g., a job that runs nightly to compute yesterday’s summary metrics or to update aggregates.
    * **Real-time Processing:** e.g., update running totals as events come (maybe using streaming tech or in-memory caching).
    * **Analytics Engine:** either a specialized OLAP database or using the relational DB with optimized queries or possibly an in-memory engine for computing metrics on the fly.
  * We might implement certain calculations here so they are pre-computed rather than at query time (especially expensive ones like cohort analysis or CLV which might be done weekly, etc.).
  * If using a data warehouse (like BigQuery, Redshift, etc.), this layer would transform and load data there. However, given this is a SaaS for many customers, a multi-tenant warehouse or partitioned data approach is needed. Alternatively, we can stick to a standard SQL DB if volume manageable or use something like ClickHouse/Druid for analytics.
  * This layer also handles **data normalization**: ensuring data from different channels can be compared (e.g., converting timezones of different sources to a common reference, or mapping product IDs from different sources if needed).

* **Storage Layer:**

  * **Operational Database:** likely a relational database (PostgreSQL/MySQL) storing things like user accounts, configuration, raw records of orders, customers, etc.
  * **Analytics Database:** possibly the same as operational or a separate optimized store for queries (could be a star schema data warehouse or an OLAP store). If the same, then careful indexing and possibly use of materialized views or summary tables for heavy queries.
  * **Data Warehouse** (optional): If data is huge, use a columnar store or big data solution for analytical queries, and keep the relational DB for small data (user config, etc.).
  * **Caching Layer:** Redis or similar to cache session data (for users) and query results that are expensive. Also possibly to queue recent events for quick aggregation.

* **Application Layer (Backend):** The server-side application (could be built with frameworks like Node.js, Django/Flask (Python), Ruby on Rails, etc.). This contains:

  * **RESTful API** endpoints that the front-end calls to get data. E.g., `GET /api/dashboard/overview?date_range=30d` would return JSON of all needed KPI values and chart data.
  * **Internal Services:** modules handling each integration (e.g., a service for Shopify data, one for Facebook, etc.), business logic for computing KPIs, applying attribution, etc.
  * **Authentication & Authorization** logic (ensuring each request is authenticated and data filtered by user’s store permission).
  * It may also include an **admin module** (for our support team to manage accounts, or for user management).
  * Documentation of this API is needed as part of technical requirements (the prompt says “API documentation (Shopify, RESTful, webhook handling)” – likely we need to specify which Shopify APIs and webhooks we use and also that we will provide our own REST API documentation for any integration or output).

* **Frontend Layer:**

  * This is the web client (likely a Single Page Application using React, Vue, or Angular, or even server-rendered if simpler, but SPA is common for dashboards for a smoother experience). It communicates with the backend via the REST API (or GraphQL if we design one).
  * The front-end code will be delivered as a web app accessible via browser, possibly embedded in Shopify Admin (Shopify apps can render inside an iframe in Shopify’s admin – using Shopify App Bridge).
  * We must ensure compatibility with the Shopify admin integration if needed (meaning handling the OAuth handshake, loading within iframe with appropriate headers etc.).

* **Integration Points:**

  * **Shopify Integration:** We will likely create a Shopify Public App that merchants install. During install, we get an API key (access token) for their store. We subscribe to webhooks (orders/create, orders/updated, etc., and GDPR webhooks) in the Shopify App setup. We will use the Shopify REST Admin API and/or GraphQL API to pull additional data (like historical orders on first sync, product list, etc.).

    * The **Shopify APIs** of interest:
      *Orders*: to get orders (with line items, discounts, etc.),
      *Customers*: for CLV and segmentation,
      *Products*: for names, categories, costs if using product meta or cost field in Shopify (Shopify Plus has product cost).
      *Analytics*: Shopify has some analytics endpoints but we might not need those if we compute ourselves.
      *Webhooks*: as mentioned.
      Possibly *Checkouts* if capturing abandoned checkouts via API (Shopify has an Abandoned Checkouts API that might be used to get abandoned cart data).
    * *API usage example:* To fetch orders, the endpoint is GET `/admin/api/2023-04/orders.json` or GraphQL equivalent. We will document that the system uses these endpoints under the hood, respecting Shopify rate limits of 2 calls/second (GraphQL has a cost-based limit). For large historical fetch, use pagination (since Shopify returns max 250 orders per page).
    * The app must handle OAuth with Shopify: initial installation will direct merchant to grant scopes (we request read\_orders, read\_products, read\_customers, etc.). After auth, Shopify redirects with a code which we exchange for permanent token. We store token for use in API calls. This is standard Shopify OAuth flow.
    * *Webhook Handling:* Implement endpoints such as:

      * `/webhook/orders/create` – on receiving, parse the order payload (JSON), store the new order in our database (or queue it for processing).
      * `/webhook/orders/updated`, `/webhook/orders/delete` if needed (though deletion likely just mark canceled).
      * `/webhook/customers/redact`, `/webhook/shop/redact`, `/webhook/customers/data_request` – handle GDPR as specified.
        Each webhook will be verified (Shopify signs with HMAC, we verify using app secret to ensure authenticity).
        We will document these in API docs, e.g., “Our system will subscribe to Shopify’s webhooks: orders/create, etc., which POST data to endpoints on our server. The webhook data structure is as per Shopify’s documentation. We process these to keep our data in sync.”
    * Using **GraphQL vs REST:** GraphQL can fetch more data in one roundtrip (e.g., get orders with selected fields and maybe nested data). We might use GraphQL for efficiency especially during initial sync. E.g., query all orders updated since a cursor with fields id, createdAt, totalPrice, customer{id,email}, lineItems {...}, etc. GraphQL has complexity limits but can be tuned.

  * **Facebook/Meta Ads Integration:** We will use Facebook Marketing API:

    * We need an App registered with Facebook to get API keys.
    * Use OAuth for the user to grant our app access to their ad account data (scopes like ads\_read).
    * Once token is stored, call Graph API endpoints like `/v13.0/<ad_account_id>/insights` with fields=spend, impressions, clicks, etc., broken down by campaign. Possibly daily breakdown as needed.
    * These calls might happen in a scheduled job, since webhooks aren’t available for performance metrics. (Facebook has webhooks for lead forms etc., not relevant here).
    * Document that: “System calls Meta Ads API to retrieve daily insights for campaigns. For example, to get yesterday’s data it calls the Insights endpoint with date\_preset=yesterday. The data is stored in our database linked to campaign and date.”

  * **Google Ads Integration:** Use Google Ads API or Google Ads Query Language (GAQL). This requires OAuth via Google and then using their client libraries. The system will likely run a daily job to fetch campaign stats (cost, clicks, conversions, etc.).

    * Document ex: “Uses Google Ads API: Service CustomerReports to fetch metrics like cost\_micros, clicks, conversions for specified date range.”
    * We have to handle OAuth token refresh for Google (they expire tokens and give refresh tokens).

  * **Mailchimp/Klaviyo Integration:** These have REST APIs (e.g., Mailchimp’s /reports for campaigns). We’d call those endpoints after a campaign is sent (could poll daily for new campaigns or webhook if they provide event hooks for “campaign sent”).

  * **Internal API (for UI):** We will design endpoints to serve the front-end. Possibly a GraphQL API for flexibility or REST with specific endpoints. E.g.,

    * `GET /api/kpi_summary?store_id=X&date_start=...&date_end=...` returns JSON of all main KPIs.
    * `GET /api/orders?store_id=X&start_date=...&end_date=...` to get raw order list for table (with pagination).
    * `GET /api/marketing/ads?store_id=X&platform=facebook&date=...` to get ad metrics.
    * Or we implement GraphQL where front-end can query exactly what it needs (which is somewhat aligned with our multi-source aggregated data model).

  Document these for developers: For example:

  ```plaintext
  GET /api/dashboard/overview
  Query Params: store_id, start_date, end_date, [optional filters like channel]
  Response: JSON with keys like:
    "total_sales": 12345.67,
    "orders": 321,
    "conversion_rate": 2.5,
    "series_sales_per_day": [ {date: ..., value: ...}, ... ],
    "sales_by_channel": [ {channel: "Direct", value: ...}, ... ],
    ... etc.
  ```

  Each endpoint’s purpose will be explained in technical documentation.

* **Data Pipeline & Workflow:**

  * **Initial Sync:** When a new store connects, trigger a background job to fetch historical data:

    * Possibly fetch last 1 year of orders from Shopify (to limit scope, or allow user to specify range).
    * This may be chunked (page through orders) and could take time, so mark the store as “syncing” with progress.
    * Similarly, fetch recent campaign history from ad platforms (maybe last 30 days or user-specified).
    * During this time, populate the database. Only once complete (or partially through) do dashboards show full data. We might show partial or at least notify user.

  * **Ongoing Data Feed:**

    * Shopify orders come in via webhook in real-time; we process them: update running totals, insert into DB, recalc any dependent metric (or mark for recalculation).
    * A nightly job might reconcile data (Shopify webhooks theoretically ensure we have all orders, but to be safe, maybe once a day we fetch any orders that might have been missed or updated).
    * Marketing data is fetched daily to update yesterday’s and today’s stats (since conversions might be reported late).
    * Web analytics events stream in continuously; we could aggregate them by session in near real-time (maybe store raw events and also increment counters for page view metrics).
    * Use of an analytics library or custom code to compute metrics from events (like count sessions, etc.). Possibly use something like Matomo (self-hosted analytics) integrated, but likely simpler to implement directly.

  * **Analytics Computation:**

    * Some metrics are straightforward (sum, counts). Those can be either calculated on the fly with database queries (if performance allows) or precomputed for dashboard quick load.
    * More complex metrics (conversion rate, abandonment) we can compute on the fly since they are ratios of counts we have.
    * CLV might need a formula spanning entire customer history – can compute when needed or have a nightly update per customer after each day’s end.
    * Multi-touch attribution requires storing each touchpoint sequence per user. That means our web analytics tracking has to log sessions with a user (even if anonymous, assign an ID if possible). Perhaps for known users (when they purchase, we can link all their past session IDs that match their email or a cookie). This is complex but doable: store a table of session events with user or prospective user id, and order id if converted. Then a query or script to evaluate attribution by model. We might not do this in real-time on every load due to complexity; possibly run a job that assigns fractional conversion credits to each campaign-touch per order at night. But if simpler, implement last-touch attribution easily (just use the order’s source).
    * We will specify: *The system will use a combination of pre-aggregated tables for performance-critical metrics (like daily sales totals, which can be summed quickly in advance) and real-time calculation for metrics that can be derived quickly from those aggregates.*

* **Third-party libraries and tools:**

  * Possibly use analytics libraries or services. E.g., we might consider using a service like Segment for data collection, but since we are building an analytics product, likely we handle the pipeline ourselves to not depend on external.
  * Chart rendering on frontend likely via a library (Chart.js, D3, Highcharts, etc.).

* **DevOps & Environment:** The system will be deployed likely on a cloud provider (AWS, GCP, etc.). We might mention using Kubernetes or serverless for scale, but depends on tech choices. Not strictly required here but note we plan for containerized or cloud deployment.

*(We would include an architecture diagram here to illustrate the above, showing boxes for Shopify, our app’s components, databases, and arrows for data flow. Since we can’t embed a new diagram easily, the description suffices.)*

### **5.2 Shopify API Integration Details**

As a critical part of the product, here are the specifics of how we integrate with Shopify (this can serve as a mini “API documentation” for the Shopify part):

* **App Authentication (OAuth):**

  * Our app will use Shopify’s OAuth2. During installation, we request the following access scopes:
    `read_orders, read_customers, read_products, read_analytics` (if needed), `read_checkouts` (for abandoned cart data), `read_shop_metadata` (maybe for store info like timezone, currency).
  * After user approves, we receive a permanent token which we store encrypted.

* **Shopify API Endpoints Used:**

  * **Orders:** `GET /admin/api/{version}/orders.json?status=any&limit=250&page=X` (for REST) or GraphQL query like:

    ```
    {
      orders(first: 250, after: $cursor) {
        edges { node { id name createdAt totalPrice customer { id email } lineItems { ... } etc. } }
      }
    }
    ```

    Used to fetch orders in initial sync and to fetch updates if needed. We store relevant fields in our database (order id, created\_at, financial\_status, total, etc., plus relational link to customer and products via line items).
  * **Customers:** `GET /admin/api/{version}/customers.json` to fetch customer list or specific customer. We might fetch these to get customer attributes (like lifetime spend which Shopify might provide, or we calculate ourselves).
  * **Products:** `GET /admin/api/{version}/products.json` to get product names, SKUs, etc., so our reports can display product titles. Also to get cost of goods (Shopify has a `cost` field in variants if the merchant uses it, which can feed profit calculation).
  * **Abandoned Checkouts:** `GET /admin/api/{version}/checkouts.json` – this gives abandoned cart data (contact info, line items, but no order). We could use this to compute cart abandonment more directly or to list items in abandoned carts. Shopify triggers `checkouts/create` webhook when a checkout is started (entered contact info) which we can leverage to count abandoned checkouts that never became orders.
  * **Shop Info:** `GET /admin/api/{version}/shop.json` for shop details like name, currency, timezone, plan. Currency is needed for displaying symbols, timezone for aligning data times, etc.
  * **Analytics (maybe):** Shopify has analytics APIs for reports but they often require higher plan. We likely do not need them as we compute ourselves.
  * All API calls will include the access token in header and be subject to Shopify API call limit (40 points per second for GraphQL, or 2 calls per second for REST). Our sync code will have throttling logic to respect these.

* **Webhook Subscriptions:** Our app (via the Shopify admin or API) will register for:

  * `orders/create`
  * `orders/updated` (to catch paid status, refunds, cancellations)
  * `orders/delete` (if an order is deleted, remove it or mark canceled in our DB)
  * `customers/create` (optional, can just get from orders, but if we want customer created without order scenario)
  * `customers/delete` maybe, though rarely used.
  * `checkouts/create` (for abandoned checkouts start)
  * `checkouts/update` (maybe to track if they completed? if completed, it becomes an order anyway)
  * GDPR webhooks: `customers/data_request`, `customers/redact`, `shop/redact`.

  When creating these webhooks, we must provide our endpoint URL and verify the HMAC when receiving. The system should log webhook events and responses for debugging.

* **Data Model Aligning:** We map Shopify data to our internal schema:

  * Use Shopify’s unique IDs (perhaps the GraphQL global id or the numeric ID) to ensure we don’t duplicate records on re-import.
  * Keep references: order to customer, order to many products.
  * If a store uninstalls the app, per `shop/redact` we wipe their data. If they reinstall, that’s a fresh integration (no historical data unless they re-sync).

* **Shopify Rate Limit Handling:**

  * In initial sync, if many orders, we will delay between calls to not exceed 2/sec. If GraphQL, use the cost mechanism – e.g., retrieving 250 orders might cost X points, ensure we wait for bucket refill if needed. Implement exponential backoff on 429 Too Many Requests responses.
  * Because webhooks push new data, we mostly avoid heavy polling after initial sync.

### **5.3 External API Integration Details**

**Facebook (Meta) Ads API:**

* Use Graph API endpoints such as:

  * `/{ad_account_id}/insights` with parameters: fields (like “impressions,clicks,spend,actions”), breakdowns (like “campaign\_name” if we want per campaign).
  * We will need the Ad Account ID from the user (which we can get via API once they authorize – listing their accounts).
  * Data comes in JSON; we parse into our tables: e.g., a table for AdInsights with columns: date, campaign, impressions, clicks, spend, purchases (if tracked).
  * If the user has the Facebook Pixel installed on their Shopify, the Pixel reports conversions to Facebook. We might retrieve “actions” field which includes “offsite\_conversion.fb\_pixel\_purchase” count and value, which is essentially what Facebook tracked as purchases. However, to avoid confusion, we might rely on our own attribution linking rather than Facebook’s numbers. Still, we can record it for cross-check or use in ROAS if user didn’t integrate attribution differently.
  * The API requires including an access\_token. That token is tied to our app and user. It expires every \~60 days (if using offline access). Our system must refresh it (store refresh token or use long-lived token and manage it).
  * Document in technical: “Calls Meta Graph API v13.0, specifically the Insights endpoint for each ad account daily. Data granularity: daily (so we get timeseries). Also fetch campaign metadata (campaign names, etc.) from /campaigns endpoint to map ID->Name.”

**Google Ads API:**

* Use the Google Ads API (which uses gRPC via client libraries or REST via their endpoints but with a token).
* We need developer token from Google and a Client ID/secret for OAuth.
* After OAuth, we get refresh token. We use client libraries likely in our backend to query Google Ads.
* A sample query might be:

  ```
  SELECT campaign.name, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions, metrics.conversions_value 
  FROM campaign 
  WHERE segments.date DURING LAST_7_DAYS
  ```

  We will run such queries daily for the prior day or for the range needed.
* Then we map campaign to results. Google Ads also can track conversions if properly configured (like conversion tracking ID).
* Possibly integrate with Google Analytics (less needed if we do our tracking).
* Document: We will use the officially supported Google Ads API libraries to fetch performance metrics on a set schedule. Because Google’s API quotas and complexity, we should ensure only to fetch necessary data. Possibly allow user to input which conversion action in Google corresponds to purchases, if they track in GA or via Google Ads conversion tracking (but probably out of initial scope; easier is just to fetch cost and clicks, then rely on our attribution to tie to conversions).

**Email (Mailchimp/Klaviyo) API:**

* Mailchimp: use `/reports` to get opens, clicks, etc. It’s straightforward REST with API key.
* Klaviyo: they provide metrics via their API too (Klaviyo can send metrics of emails and even has attributions for sales if connected to Shopify).
* This integration might need an API key from the user (like Mailchimp API key or Klaviyo private token).
* We’d document: “The system calls Mailchimp’s campaigns list endpoint to get campaign IDs and then fetches each campaign’s report (opens, clicks, etc.). These are stored in the `email_campaigns` table and linked by campaign id. The system matches campaign by naming convention or via UTM parameters to actual sales.”
* Matching logic: If an email campaign “Holiday Sale” was sent on Jan 1, and it had UTM campaign “holiday-sale”, then for any orders we find with utm\_campaign=holiday-sale (from our web tracking or Shopify referring site), we attribute to that email. We might have to process that linking logic in our data pipeline.

**Web Analytics Implementation:**

* The system will provide a small JS snippet, e.g.:

  ```html
  <script>
    !function(){var e=window.analyticsEcom=window.analyticsEcom||[];if(!e.initialize){
      e.invoked = true; e.methods = [...]; e.factory = function(t){ return function(){ e.push([t, ...arguments]) } };
      // define methods like e.track = e.factory('track'), etc.
      e.load = function(key){ ... } 
      e.load('XYZ123');  // some key for the site, or we embed config
    }}();
  </script>
  ```

  This is similar to Segment or GA snippet. It collects page info and sends to our endpoint.
* Or simpler, we instruct adding a script tag `<script src="https://ourcdn.com/analytics.js" data-key="STORE123"></script>` which auto-inits tracking.
* This script will on page load send a `pageview` event with URL, referrer, and maybe if logged in (Shopify might have customer id on front-end if we expose it), etc.
* It will store a cookie with a visitor ID to track returning vs new.
* Also track special events: when user clicks add to cart, etc. Possibly we provide a small snippet to attach to the Shopify theme’s Add to Cart button or listen to Shopify’s JavaScript events (Shopify has a global object for the cart that could be tapped).
* Technical: we’ll build an endpoint like `/collect` in our backend that accepts events (with store\_id, event\_type, and data). We’ll likely batch events in the client to send in one go to reduce network overhead (like Segment’s analytics.js does).
* For identifying user: If a visitor logs in or enters email at checkout, we could call an identify event so that their cookie ID links to that email or customer ID. This way, if they purchase, we know their previous visits belonged to that customer. This is needed for multi-touch attribution across sessions.
* Data storage for events: possibly a table `events` with columns (store\_id, visitor\_id, session\_id, timestamp, event\_type, page, referrer, etc., plus maybe associated order\_id if it's a purchase event).
* Then we can derive sessions by grouping events by session (session could be tracked by our cookie with a session expiration of 30 min inactivity).
* We might not want to store raw pageview of every user indefinitely to save space. Perhaps summarize daily unique visitors and pageviews after some time (or allow raw data retention for a period like 90 days, older gets aggregated).
* This will be addressed in Data retention in Data Storage section.

### **5.4 Data Pipeline Architecture and Analytics Engine**

The analytics engine refers to how queries are executed to get the results needed for the dashboards. We have options: directly query the relational DB, or have a separate OLAP engine.

For an MVP, we might implement within a relational DB using SQL queries with appropriate indices. If performance becomes an issue, consider introducing an OLAP solution.

**Analytics Query Handling:**

* For each dashboard, we can either pre-compute or compute on demand:

  * For example, Total Sales for period X: a SQL `SELECT SUM(total_price) FROM orders WHERE store_id = ? AND created_at BETWEEN ? AND ?`.
  * Conversion Rate: needs both orders count and sessions count. Orders count from orders table, sessions count from sessions table (if web analytics integrated). We can do two queries or one if we store aggregated data daily.
  * Many metrics can be gotten by grouping or filtering queries. We need to ensure these are optimized (indexes on date, etc.).
* Possibly create **materialized views** or summary tables:

  * e.g., a daily summary table per store with columns date, total\_sales, orders\_count, sessions\_count, etc. That gets updated each day (yesterday’s data gets a row). Then queries for last 30 days are trivial (select those 30 rows and sum or whatever).
  * But real-time data (today’s partial) still needs live computation from events or orders.
  * We can maintain a running today total in memory or cache.
* The engine should handle multi-tenant by partitioning data by store (either in separate schema, but easier just include store\_id in every key and index queries by store\_id).
* **Use of Data Warehouse**: If using something like BigQuery, we could offload heavy queries (like “give me last 5 years of data by month”). But the overhead might not be worth initially; simpler is a well-indexed Postgres or MySQL.
* Ensure to analyze query plan for key queries to add indexes (like index on orders(store\_id, created\_at), on sessions(store\_id, date), etc.).
* Possibly use a search engine or analytics engine for specific things: e.g., if wanting to filter orders by many criteria quickly, an Elasticsearch or so could help. But likely not needed if DB is fine.

**Data Volume Consideration**:

* If a store has 100k orders/year, 5 years = 500k orders. That’s not huge for a database to sum or count quickly if indexed. Even 1 million orders is fine on a decent DB server for aggregation queries (especially if partitioned by store).
* Web events might be larger (say 1M pageviews per year for a busy site). But aggregated to sessions maybe 300k sessions/year. Still okay if using proper summarization.
* So our chosen approach is to carefully design DB and queries with performance in mind to avoid needing a big data pipeline for now. But design such that if we needed to swap out the back-end (e.g., move heavy data to a column store), the front-end and API wouldn’t change, just the implementation of the data layer would.

**API Documentation (for our API):**

* We will produce a document for developers (if we expose our API or just internal dev).
* If we plan to let merchants pull data via API (maybe to feed into their own warehouse), we should define those endpoints and perhaps consider implementing a GraphQL API which is often convenient for analytics (like Shopify’s own GraphQL).
* But since not explicitly asked, likely the “API documentation” referred is how we integrate with others, which we’ve described, and ensuring our own API is well-documented internally.

### **5.5 Workflow for Role-Based Access**

(Though roles are primarily functional, technically we need to implement it.)

* Our backend should have a concept of Users and Organizations (Organization might represent the Shopify store or company).
* A User belongs to an Organization with a Role (Admin, Analyst, Manager).
* When that user makes requests, the backend checks their role:

  * e.g., if hitting an endpoint to invite user, only Admin role allowed.
  * If trying to change a setting, maybe only Admin.
  * Viewing data likely allowed to all roles in that org (with differences noted in Section 6).
* If we allow cross-store users (like an agency with multiple stores), we might model that either as separate organizations and a user can belong to multiple, or treat it as one org with multiple stores attached. We need to clarify:

  * Likely, each Shopify store is an “Org” because data is separate. If an agency wants combined, they might have an Org that links multiple stores (meta-organization concept). We might not implement that initially unless demand.
* Authentication token (JWT or session) should carry user id and org id to enforce scope on every request.

### **5.6 Logging and Monitoring**

Technically, include components to log activities:

* Use a logging framework to record info (with PII stripped or hashed as needed).
* Monitor API usage and errors. Possibly integrate with a service like Sentry for error tracking in front-end and back-end.
* Track events like each time a webhook is received and processed count (to monitor if we fall behind).

### **5.7 Development & Testing Requirements**

While not always in SRS, we can mention:

* The system should be developed in a way that it’s easily testable. Provide unit tests for critical calculations (e.g., test that conversion rate calc yields correct output for given inputs).
* Provide integration tests for data ingestion (simulate a webhook payload and ensure the data goes to DB).
* Perhaps support a sandbox mode (for development using Shopify’s dev store and test data from ad APIs).
* Ensure environment variables or config files hold secrets (Shopify API secret, DB passwords, etc.), not hard-coded.

### **5.8 Deployment and Maintenance**

* Provide instructions for deploying new versions. Possibly continuous integration pipeline that runs tests and deploys.
* The system should be able to be updated without downtime. Achieve this by either deploying new instances then switching traffic (blue-green deployment) or using rolling updates if stateless.
* The database migrations (if needed) should be planned to not lock tables for long, or done during low-traffic.
* We should plan a maintenance window for bigger updates if needed and communicate via status.

This technical design aims to satisfy all functional requirements with a reliable and maintainable system. The exact technology stack (programming language, database) can be decided in the implementation phase, but the architecture described ensures separation of concerns and scalability for the core tasks: data ingestion from multiple sources, data storage, analytics computation, and serving the results to users in real-time.

## **6. User Roles & Permissions**

The system will implement role-based access control (RBAC) to manage what different types of users can see and do within the application. There will be three primary roles: **Admin**, **Analyst**, and **Manager**. Below we define each role and their permissions, and how the system enforces these.

**Role Definitions:**

* **Admin:** This is the super-user for a given organization (Shopify store account). Typically the store owner or the person who installed the app. They have full access to all data and settings.
* **Analyst:** A user who can view and analyze data, create and edit dashboards, but has limited administrative privileges. They usually cannot change high-level settings or manage users.
* **Manager:** This could be a view-only or limited-edit role aimed at managerial stakeholders who want to see reports but not necessarily modify configurations. (The name “Manager” is a bit generic; we interpret it possibly as a role that can view data and perhaps create basic reports, but not alter system settings or integrations.)

We can adjust the exact permission for Manager vs Analyst based on typical needs: sometimes an “Analyst” might do deeper analysis (create custom dashboards, export data) whereas a “Manager” might just view existing dashboards and maybe schedule reports.

**Permission Matrix:**

Below is a table outlining what each role can do:

| **Feature / Action**                                    |         **Admin**         |      **Analyst**      |                       **Manager**                      |
| ------------------------------------------------------- | :-----------------------: | :-------------------: | :----------------------------------------------------: |
| **View Dashboards and Reports**                         |         Yes (all)         |       Yes (all)       |                        Yes (all)                       |
| **Customize/Create Dashboards**                         |            Yes            |          Yes          |  *Limited* (perhaps can create personal views or none) |
| **View All Data (all channels, metrics)**               |            Yes            |          Yes          |                           Yes                          |
| **Add/Edit Integrations (connect APIs)**                |            Yes            |           No          |                           No                           |
| **Manage Users (invite/remove)**                        |            Yes            |           No          |                           No                           |
| **Change System Settings (e.g., data retention, plan)** |            Yes            |           No          |                           No                           |
| **Export Data (CSV, PDF)**                              |            Yes            |          Yes          |                           Yes                          |
| **Schedule or Email Reports**                           |            Yes            |          Yes          | Possibly yes (if it's just scheduling existing report) |
| **Delete Data or Reset**                                |            Yes            |           No          |                           No                           |
| **Access API (if separate API token)**                  | Yes (can generate tokens) | Possibly (if allowed) |                    No (or view only)                   |
| **Administrative Dashboard (if any)**                   |            Yes            |           No          |                           No                           |

*(The exact distribution can be tweaked; for example, maybe Manager can’t create dashboards but can still export, etc. We clarify below.)*

**Admin Permissions Detail:**

* Admin can do everything: connect or disconnect integrations (Shopify is connected by default but e.g., add Facebook account or remove it), configure settings like default currency if needed, and manage team members.
* They see all dashboards and can create/edit or delete them. They might also designate which dashboards are shared to others or private.
* Only Admin can invite new users to the platform (Analysts and Managers cannot invite or remove users).
* Admin can assign roles to invited users. (By default, the one who installs app is Admin).
* Admin can change subscription or billing details if this SaaS has a paid plan (outside scope maybe).
* Admin can handle data retention settings (if we allow, maybe by default we keep all data; if an admin wants to purge some data, they can).
* In terms of data, Admin sees everything relevant to their store. (They cannot see other stores’ data unless they have Admin rights on those too).

**Analyst Permissions Detail:**

* Analysts have full read-access to all data (they can view all dashboards and drill into all reports – orders, customers, etc. There may be some sensitive data like individual customer info; since they are likely employees or contractors, this is allowed by Admin’s trust, but if needed we could have a role that hides customer PII – not specified though).
* They can create new dashboards or custom reports for deeper analysis. They can save these for themselves or possibly share with team (but maybe only Admin can publish a dashboard to team view; we could decide if Analysts can share their dashboards to others or only to Admin for approval).
* They can export data for analysis offline (CSV downloads of, say, all orders or KPI trends).
* They **cannot** manage integrations or users – so they cannot accidentally break data connections or invite someone.
* They also cannot delete data or do destructive actions (other than maybe deleting a custom dashboard they created).
* If the system has any configuration for metrics (like define a custom metric formula), likely only Admin can do that; Analyst uses what's provided.

**Manager Permissions Detail:**

* Managers in this context likely are business managers who want to see reports but not fiddle with the system. So:
* They have read-only access to all standard dashboards and reports.
* They typically would not create new dashboards (but maybe they can create a custom view for themselves if non-technical? Unlikely – possibly they rely on Analysts to do it).
* Let’s assume *Manager is basically a “View Only” role.* They can apply filters on dashboards interactively but cannot save those changes or alter the underlying dashboard for others.
* They can export or print reports (since a manager might need to include a chart in a meeting, etc.).
* They cannot change any settings, cannot manage users, cannot connect integrations.
* Essentially, they log in and consume the data that’s there.
* If a Manager tries to access an area they shouldn’t (like Settings), the UI should hide it or gray it out, and if forced, the backend rejects it with a permission error.

**Enforcement:**

* The front-end will show/hide controls based on role:

  * e.g., only Admin sees the “Settings” menu item.
  * Only Admin sees the “Invite Users” button in user management.
  * Analysts might see an “Edit Dashboard” button, Managers will not.
* The backend will always verify permission too (never rely solely on front-end). Each API endpoint will check the user’s role from their session.

  * e.g., `POST /api/dashboard/update` will check `if user.role != Admin/Analyst: return 403 Forbidden`.
  * `POST /api/user/invite` will check `if user.role != Admin: 403`.
* Possibly use a middleware or decorator to restrict by roles easily.

**Multi-Store scenario:** If one user is admin of multiple stores, they would have separate contexts. Perhaps they have to switch context in the UI (select a store to view). When in one store context, they get the role they have for that store.

* If a user is Admin on Store A and Analyst on Store B, when they switch to Store B, the UI should adjust to Analyst-level (i.e., hide user management etc. for that store).
* We'll manage this by scoping user-role by store in our data model (like a join table user\_org with role).

**Role Assignment & Changes:**

* Only Admin can promote or change roles of other users. Possibly in UI: an Admin can change an Analyst to Manager or vice versa (except cannot change themselves to non-Admin if that would leave no Admin).
* If a user leaves the company, Admin can remove them (they lose access).
* We should ensure at least one Admin exists per organization for safety.

**Audit & Security:**

* Keep track of which user did actions like changed settings or invited someone (for accountability).
* Ensure that if an Admin role is transferred (like original admin leaves, they designate someone else as admin), the system handles that smoothly.

In summary, the roles ensure a **separation of concerns**:

* Admin deals with configuration and has full control.
* Analyst deals with analyzing and configuring reports but not core settings.
* Manager (or sometimes called “Viewer”) can consume the insights without altering configuration.
  This structure fits typical e-commerce teams where the store owner/IT lead is Admin, a marketing analyst or data scientist is Analyst, and maybe an executive or regional manager is just viewing the results.

## **7. Data Storage and Reporting**

This section addresses how data will be stored, managed, and retrieved for reporting purposes. It covers the database design considerations, data retention, as well as the capabilities for exporting data out of the system in various formats (CSV, PDF, etc.), which is important for users who want offline analysis or to share reports.

### **7.1 Data Storage Design**

**Database Choice and Structure:** The system will use a **relational database** as the primary data store (e.g., PostgreSQL for its reliability and analytical query strength). The schema will be designed to accommodate multi-tenant data (each merchant’s data tagged by a store id or in separate schema if we choose).

Key tables (or collections if NoSQL chosen, but likely SQL):

* **Stores (Tenants):** store\_id, store\_name, Shopify shop domain, currency, timezone, etc.

* **Users:** user\_id, name, email, password\_hash (if not using Shopify SSO), etc.

* **UserRoles:** mapping of user to store and role.

* **Orders:** capturing Shopify orders. Fields might include order\_id (Shopify ID), store\_id, order\_number, date/time, total\_price, subtotal, tax, shipping, discounts, financial\_status, fulfillment\_status, customer\_id (foreign key to Customers table), etc. We may also store channel info if an order is from another channel (perhaps via a field “channel” which for native Shopify store orders = “Online Store”, others might be “Amazon” etc. If we import orders from Amazon separately, they also go here with channel tag).

* **OrderLineItems:** order\_id, product\_id, product\_name (storing name for snapshot), quantity, price, discount\_allocations, etc. This helps with product-level reporting.

* **Customers:** customer\_id, store\_id, name, email (if not storing full, maybe partial for privacy), first\_order\_date, last\_order\_date, total\_orders, total\_spent, etc. We might maintain aggregate fields to speed up CLV calculation (like a field total\_spent which is sum of all orders by that customer).

* **Products:** product\_id, store\_id, title, SKU, category (if any), cost (if available), etc. and possibly current inventory level if we pull that periodically. We store product info to enrich order line items and to do product performance reports.

* **AbandonedCarts (Checkouts):** if we track checkouts that didn’t convert: could store checkout\_id, customer\_or\_email, created\_time, items (maybe as JSON or a separate table), and maybe an abandoned\_flag if not converted. This helps create abandonment metrics or follow-ups. Alternatively, we derive abandonment metrics from orders vs. cart events rather than storing each, since that’s less critical to list out.

* **Sessions/WebTraffic:** If we do our own tracking, a table for sessions: session\_id, store\_id, visitor\_id, start\_time, end\_time, number\_pageviews, referring\_source, device, etc. Or we might store raw events in an **Events** table (with type pageview, click, etc.) and then generate sessions on the fly or via batch. Storing sessions aggregated is easier for analytics queries. We could have:

  * *Visitors:* visitor\_id and maybe link to customer (if identified) and first\_seen, last\_seen, etc.
  * *SessionEvents:* as raw events.
    But more likely: we will store aggregated daily data for visits in a **TrafficDaily** table: date, store\_id, total\_sessions, total\_pageviews, bounce\_count, etc., for quick daily trend queries, while optionally keeping raw events for deep dive (maybe temporarily).

* **Marketing/Ad Data:** separate tables for each integration or a unified one with type:

  * e.g., **AdCampaignStats:** id, store\_id, platform (Facebook, Google, etc.), campaign\_name (or ID), date, impressions, clicks, spend, conversions, revenue (if we choose to import their reported revenue or our attributed revenue).
  * **EmailCampaigns:** campaign\_id, store\_id, campaign\_name, send\_date, emails\_sent, open\_rate, click\_rate, etc., and maybe attributed orders count & revenue (which our system calculates via matching).
  * We might also store raw campaign messages for reference (subject line, etc. in an EmailCampaign table, with a one-to-many to stats per send).

* **Aggregates & Derived tables:**

  * **DailySalesSummary:** store\_id, date, gross\_sales, net\_sales, orders\_count, new\_customers\_count, etc. (populated daily).
  * **MonthlyMetrics**: store\_id, month, these metrics (for quick monthly reporting).
  * **FunnelStats:** store\_id, date, sessions, add\_to\_cart\_count, reached\_checkout\_count, completed\_purchase\_count, computed conversion rates.
  * Or we can compute funnel on the fly from events, but storing doesn’t hurt since it’s a small data.
  * **CustomerLifetimeMetrics:** could store each customer’s CLV updated, or just calculate when needed from orders.

* **Data Partitioning:** All these tables should have an index on store\_id for isolation. We could also physically partition by store (some DBs allow table partition per key). But given potentially thousands of stores, that might be heavy. Simpler is index and include store\_id in composite index with date for large tables like orders/events (because queries will often filter by store and date range).

* **Data Volume & Retention:**

  * Order and customer data we likely keep indefinitely (merchants expect year-over-year comparisons etc.). We will not delete or roll these up except if store is deleted (then we purge for GDPR).
  * Web analytics raw data (page views): We might keep raw events for a limited time (say 1-2 years) to prevent DB from growing too large. After that, we might aggregate or delete detailed events and keep summary stats. We will define this in retention policy. Possibly allow the merchant to request longer retention if on a higher plan.
  * Ad data: could be re-fetched if needed, but we will store historically so that even if they disconnect integration, past data remains for context (maybe mark it stale). Ad data is usually not extremely large for a single store (couple campaigns per day, aggregated daily).
  * If using any logs or debug data, those might be pruned frequently.

* **Backups:** The database will be backed up regularly (e.g., daily snapshots). If using cloud managed DB, use their backup feature with point-in-time recovery. Ensure backups themselves abide by privacy (Encryption and retention of backups similarly short if store is deleted).

* **Multi-tenant Data Isolation:** Ensure that queries run by one user never mix data with another. This is done via the store\_id filter. Possibly, at the application level, use an ORM that automatically adds a tenant filter based on context. In testing, try cross-store queries to ensure none leak. This is partly security but also data integrity (we wouldn't want to accidentally combine data from two stores in one chart).

* **Scaling Storage:** If the DB grows large (e.g., many stores, tens of millions of rows), consider scaling vertically (more CPU, RAM) or horizontally:

  * Read replicas can be used to offload heavy read queries (like generating a huge report) so as not to affect the primary handling writes from webhooks.
  * Sharding by store region or ID range if needed (less likely initially).
  * For now, one decent-sized relational DB should handle the anticipated load (given each store’s data is moderate, and queries are mostly within one store).

### **7.2 Data Processing & Maintenance**

As part of storage, mention how we maintain data:

* We will have background jobs to recalc certain fields:

  * e.g., each night, go through new customers and update their `total_spent` or assign them to a cohort.
  * Each order insertion triggers maybe an update to daily summary or to customer aggregate (like increment that customer’s order count).

This ensures some reports can be instantaneous (just reading from an aggregate table instead of summing all orders each time).

However, we must avoid double-counting or missing if both realtime and nightly jobs do things; have idempotent logic (like nightly job can recalc from scratch daily totals to correct any minor drift from realtime calc).

### **7.3 Reporting and Exporting Data**

The system will provide several ways to output data for user consumption outside the app:

* **On-Screen Reports:** The dashboards and tables themselves are a form of reporting. Users can read and interact. But often, they want to extract or share data.
* **CSV Export:**

  * Every major table or data view should have an option to export as CSV (comma-separated values) for use in Excel/Google Sheets or other tools. For example:

    * Export orders list (with all details).
    * Export a summary of sales by month (two columns: month, sales).
    * Export a list of top 100 customers with their total spend.
    * Export raw events if needed (maybe not via UI, but could provide if requested).
  * The UI might have an “Export” button on relevant pages. When clicked, either download immediately if quick or start a job and email when ready (for very large exports).
  * The format should be well-structured with headers. Use UTF-8 encoding for international text.
  * Consider the number formatting: likely raw values (no currency symbol in CSV, just number or maybe separate column for currency).
  * Admin and Analyst likely can export, Manager can as well but maybe limited if needed. But since they can see it anyway, export is fine for them.
* **PDF or Printable Reports:**

  * The system should allow exporting a dashboard or specific charts as PDF or image for presentations.
  * For PDF: either generate a nicely formatted PDF with charts and tables (could be done using a headless browser screenshot or a report template).
  * Possibly allow scheduling: "Email me this dashboard as PDF every Monday".
  * If PDF generation is complex, at least provide a print stylesheet so that using browser’s print (or print to PDF) yields a decent result. Ensure dark backgrounds switch to white or such for print, etc.
  * Over time, we might create a feature: *Report Builder*, where the user selects components and generates a PDF or slide deck. But initially, maybe just a PDF of the current view or a few standard report templates (like a monthly summary report in PDF).
* **Scheduled Emails:**

  * The product could email daily/weekly summary to users. Many analytics tools do that.
  * E.g., every day at 8am, an email “Your store yesterday: \$X sales, vs day before +5%, top product..., etc.” possibly with a couple sparkline images.
  * Or a weekly report PDF attached.
  * This is a functional extension but relevant to reporting. We'll include: *The system shall support scheduling automated reports via email.* Users can configure (maybe Admin only or each user for themselves) to receive certain dashboards or metrics regularly.
  * Ensure emails are secure and only go to intended recipients. Possibly include links to log in for more details.
* **External BI Integration:**

  * Some advanced users might want to pull data into their own BI systems or data warehouse. We should facilitate this:

    * Provide an **API endpoint or data feed** for them to query data (maybe a REST API where they can fetch JSON of their data to plug into PowerBI/Tableau).
    * Or allow direct connection via a third-party connector if possible (like we might in future build a secure Snowflake or BigQuery share).
  * Initially, CSV export might suffice for most. But it’s good to note the possibility. For example, we might allow generating an API key for read-only access to their data, and then document endpoints for orders, customers, daily metrics, etc. That basically is giving them a way to programmatically export in JSON or CSV form.
* **Data Retention & Deletion (User-initiated):**

  * If a user (Admin) wants to purge some data (maybe to comply with their policies or to free space), we might allow them to delete raw event logs older than X (though they'd likely not bother, they expect us to handle it).
  * Possibly allow deleting a specific customer’s data manually (if needed outside of GDPR webhook scenario).
* **Storage Capacity / Limits:**

  * If our plan has limits (like on number of pageviews tracked for a pricing tier), we might need to enforce or at least warn. But presumably unlimited within reason.
* **Data Integrity & Auditing in Reports:**

  * The system should ensure exported numbers match what’s on the dashboard at that time (consistency). If data is being updated while exporting, we might lock or use a last stable snapshot for the export.
  * We should version changes in metric definitions or calculations so that if something changes, we can note in report (for trust).

**Examples of Exports:**

* A merchant wants to do deep analysis in Excel of sales: They go to Orders page, click Export CSV for Q4 orders, then open in Excel.
* An analyst wants to combine our data with their internal data: They use our API to fetch JSON of daily sales and load into their system.
* A manager wants to share results with a stakeholder who doesn’t have login: They export a PDF of the Monthly Performance dashboard and email it manually (or schedule auto email).

**Reports in-app vs external:**

* We might implement some custom report builder for things not shown on dashboards (like a custom cohort analysis output). But given the dashboards cover most, we probably treat dashboards as reports themselves.
* If any regulatory or accounting need, they might want to export to accounting software – out of scope likely (Shopify usually integrated with that).

**Internationalization in Reports:**

* If exporting for international, should we export numbers with locale format or standard? CSV should probably use period as decimal and comma separated as default (English). Or to be safe with Excel internationally, maybe we allow choosing delimiter (Excel in Europe often expects semicolon ; as delim). But that might be too detailed, likely just standard CSV and let them adjust.

**Data Privacy in Exports:**

* If containing personal data (like full customer list with emails), ensure only Admin or authorized roles can export such sensitive info. Possibly restrict Manager from exporting full customer list, but if they can view it on screen they could copy it anyway. So main difference is just trust and maybe logging who exported what.
* Possibly redact some sensitive columns for lower roles: e.g., Manager can view customer name but not email on screen (just hypothetical if needed). The requirements did not specify that, so we assume all roles can see all data in their store.

**Auditing Exports:**

* Maybe log when an export is done (especially if it contains personal data) for compliance, saying user X exported customer list on date Y.

**Storage of Exports:**

* Not store by us (except maybe a temp link for download after generation). It's delivered to user then gone. Unless scheduled emails, then it's in their inbox only.

### **7.4 Data Compliance and Retention Policies**

(Bringing up GDPR again in context of storage)

* We'll align retention with merchant needs and regulations:

  * Personal data like customer info will be kept as long as the store is using the service, unless deletion requested.
  * If store uninstalls, we remove data as per Shopify timeline (within 48 hours after shop/redact, personal data gone).
  * Possibly anonymize some data instead of outright deletion for aggregate stats (but safer just remove).
  * Cookie/visitor data for EU visitors: we might store an indicator if user did not consent, in which case we either not store event or mark it so we can exclude or delete those events if required.

**Backup retention**: Typically keep backups for say 30 days. After store deletion, ensure no backups beyond that that still have their data (or have a way to remove them from backups, though that’s tricky; usually allowed to keep for ops for a short period under GDPR if not accessible in production).

**Scalability of Data Storage:**

* If we have extremely large stores, consider archiving older data to separate storage. Perhaps after 5 years, move older orders to a cold storage that can be retrieved on demand (though likely not needed soon).
* If images (maybe storing screenshots of dashboards for email) we may have file storage but that’s trivial (not much of that).

**Data Warehouse Integration (if any):**

* If we choose to implement on a data warehouse like BigQuery or Snowflake, storage is their concern but basically unlimited scale. We then query that via SQL. This is an alternate approach to consider if the product scales to lots of data. But initially, our own DB should suffice.

By addressing data storage design and reporting capabilities, we ensure the system not only analyzes data but also gives merchants **full control over their data** – they can obtain copies of it, use it in other tools, and trust that it’s stored securely and in compliance with regulations. The combination of interactive dashboards and robust export options makes the analytics both actionable and shareable, fulfilling the varied needs of e-commerce businesses using the platform.
