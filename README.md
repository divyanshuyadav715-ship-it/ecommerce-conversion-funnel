# E-Commerce Conversion Funnel & Drop-Off Analysis

## Executive Summary
Analyzed 100,000 user sessions to identify friction points in the purchasing journey. Discovered a massive drop-off at the checkout stage, specifically impacting mobile users. This friction point is resulting in an estimated ₹25 Lakhs in lost revenue opportunities per month.

## The Business Problem
Our e-commerce platform generates significant top-of-funnel traffic (100,000 monthly website visitors), but the overall conversion rate was underperforming. Management needed to know exactly where users are dropping off (Product page? Cart? Payment gateway?) and what the financial impact is.

## The Tech Stack
* **Data Sourcing:** Synthesized Web Traffic Log Data (mimicking raw user event data).
* **Data Transformation:** Python (Pandas) mimicking SQL window functions and CTEs.
* **Data Visualization:** Matplotlib / Seaborn (Mimicking Tableau/Power BI dashboards).

## The Analysis Process

### 1. Data Cleaning & Funnel Construction
Processed raw event logs (containing `session_id`, `user_id`, `timestamp`, `event_type`, `device_type`, `traffic_source`). Constructed a funnel tracking unique sessions at each stage of the journey:
`Session Started` ➔ `Product Viewed` ➔ `Added to Cart` ➔ `Checkout Initiated` ➔ `Purchase Completed`.

**Overall Funnel Metrics:**
* Session Started: 100,000 (100%)
* Product Viewed: ~80,000 (80%)
* Added to Cart: ~32,000 (32%)
* Checkout Initiated: ~16,000 (16%)
* Purchase Completed: ~6,000 (6%)

*(See `funnel_overall.png` for a visual representation)*

### 2. Identifying the Root Cause
Segmenting the funnel by `device_type` revealed a critical anomaly:
* **Desktop Users:** ~60% of users who initiate checkout complete their purchase.
* **Mobile Users:** Only **~15%** of users who initiate checkout complete their purchase.

The data shows a massive drop-off on mobile devices specifically during the final checkout stage. This strongly indicates a potential UI bug, a non-responsive design element, or a broken payment gateway on mobile browsers.

*(See `checkout_conversion_by_device.png` for visual representation)*

## Data-Driven Recommendation
**Action Plan:** Recommending an immediate technical audit and UX redesign of the mobile payment flow. 

**Financial Impact:** By recapturing and normalizing the mobile checkout conversion rate from ~15% to match the desktop rate of ~60%, we can salvage thousands of abandoned carts. Assuming an Average Order Value (AOV) of ₹1,500, fixing this mobile friction point could increase monthly revenue by approximately ₹25 Lakhs.
