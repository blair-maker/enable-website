# Page titles, meta descriptions and redirects

Set these in Webflow under each page's settings. Titles are kept under 60 characters where possible and
descriptions under 155, so neither is truncated in results. New Zealand English throughout, and no page
claims anything the page itself does not support.

## Titles and descriptions

**`/` Home**
Salesforce partner, Auckland and Wellington | Enable
Enable works every layer of the Salesforce stack, from Data 360 through Customer 360 and Agentforce to AIforce. Senior practitioners, fixed pricing, no minimum terms.

**`/waypoint` Waypoint**
Waypoint: continuous Salesforce improvement | Enable
A standing programme of quarterly review, prioritisation and build for your Salesforce platform. Month to month, no minimum term. Auckland and Wellington.

**`/salesforce` Salesforce practice**
Salesforce consultancy, Auckland and Wellington | Enable
Sales Cloud, Service Cloud, Data 360, Agentforce and Agentforce Marketing, delivered by senior practitioners who ask what you are trying to do before opening the platform.

**`/about` About**
About Enable: business first, Salesforce second
We started Enable because good organisations kept ending up with platforms that were not doing what they should. The people you meet are the people who do the work.

**`/contact` Contact**
Contact Enable | Salesforce partner, New Zealand
Tell us what you are trying to do and we will tell you which layer of the stack it lives in, what it would take, and whether it is worth doing at all.

**`/storeconnect` StoreConnect**
StoreConnect on Salesforce, NZ implementation partner | Enable
Enable builds websites, online stores and point of sale natively on Salesforce with StoreConnect. One catalogue, one customer record, no middleware.

**`/lumin` Lumin Sign**
Lumin Sign for Salesforce, NZ implementation partner | Enable
Agreements generated from your Salesforce records, signed without an account, and filed back automatically. A New Zealand consultancy implementing a New Zealand product.

**`/gridmate` GridMate**
GridMate for Salesforce, implementation partner | Enable
Thirty-two Lightning components that stop your team exporting to Excel: inline editing, grids, calendars, kanban and maps on the records you already have.

**`/nonprofit` Nonprofit Cloud**
Nonprofit Cloud consultants, New Zealand | Enable
Fundraising, programme delivery, case management and outcomes on one Salesforce platform, built around how your organisation actually works.

**`/nonprofit/npsp-migration` NPSP migration**
NPSP to Nonprofit Cloud migration | Enable
NPSP remains supported and there is no forced end date, so this is a decision rather than a deadline. Start with a three-week assessment, not a migration plan.

**`/marketing-cloud-next` Marketing Cloud Next**
Marketing Cloud Next, first APAC partner to deliver | Enable
Campaigns on the core platform: audiences from Data 360, journeys in Flow, measurement without a warehouse. Seven implementations since we shipped the region's first.

**`/work` Case studies**
Our work, described honestly | Enable
Three Salesforce engagements written up without invented metrics and without client names we have not been given permission to use. References available on request.

**`/work/heritage-unified-profile`**
Case study: six systems, one supporter profile | Enable
How a national heritage organisation moved from supporter activity scattered across six systems to a single unified profile on Data 360, deployed to production.

**`/work/retirement-living-routing`**
Case study: when every enquiry reaches one person | Enable
A retirement living operator was generating strong enquiry volume, all of it landing in one consultant's queue because of a routing fallback nobody had revisited.

**`/work/first-marketing-cloud-next-apac`**
Case study: first Marketing Cloud Next in APAC | Enable
Salesforce shipped Marketing Cloud Next and Enable was the first partner in the region to put it into production. Seven further implementations have followed.

> This page is unfinished on the canvas. Either fill the bracketed sections before publishing, or leave the
> page unpublished and run `/work` with two studies.

---

## Open Graph

Same title and description on each page. For the image, crop the page's hero diagram on a white ground at
1200 × 630. That gives every page a distinct, on-brand card without commissioning anything, and the
diagrams read well at small sizes because they are already built from large shapes.

About is the exception: use the team photograph once it exists.

---

## Redirects

Site settings → Publishing → 301 redirects.

| From | To | Why |
|---|---|---|
| `/quick-starts` | `/waypoint` | Quick Starts folded into Waypoint as its on-ramp |
| `/services` | `/salesforce` | Old practice-area page |
| `/training` | `/waypoint` | Training now sits inside the how-to-start section |

Check your current site for any other live URLs before publishing. Anything with inbound links or sitting
in a campaign needs a destination, and a 404 on a page a prospect was sent to is worse than a redirect to
something approximately right.

---

## Still outstanding on the site

- **Privacy policy and terms.** The footer does not link to them yet. It should, and in New Zealand a
  contact form collecting names and emails makes a privacy statement a reasonable expectation.
- **404 page.** Worth ten minutes: heading, one line, links to Home and Contact.
- **Mobile artboards.** Only StoreConnect has one. The responsive rules in `BUILD-GUIDE.md` cover the rest,
  but if you want any page's mobile view drawn rather than described, say which.
