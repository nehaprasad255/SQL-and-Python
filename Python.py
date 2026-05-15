bash

cat << 'PYEOF' > /home/claude/build_roadmap.py
import json

# ─────────────────────────────────────────────
# RICH TOPIC DATA  (SQL + Python)
# Each topic has: name, desc, level, must,
#   why, concepts[], keycode[], realworld[],
#   interview[], tasks[], mistakes[], tips[],
#   video (YouTube embed search link)
# ─────────────────────────────────────────────

SQL_BASICS = [
  { "name":"SELECT statement & column aliases (AS)",
    "desc":"The foundation of every SQL query — retrieving columns from a table.",
    "level":"beg","must":True,
    "time":"1-2 hrs","order":1,
    "why":"Every single SQL query starts with SELECT. Mastering aliases, column expressions, and ordering is non-negotiable before anything else.",
    "concepts":["SELECT col1, col2 FROM table","Column alias: SELECT salary * 12 AS annual_salary","SELECT * — avoid in production","Expressions in SELECT: col_a + col_b AS total","DISTINCT: SELECT DISTINCT city FROM customers"],
    "keycode":["SELECT name, department, salary * 12 AS annual FROM employees;","SELECT DISTINCT country FROM customers ORDER BY country;","SELECT first_name || ' ' || last_name AS full_name FROM users;"],
    "realworld":["Pull employee names and annual salaries for a payroll report","Build a customer list with full name combined from first+last","Extract unique product categories for a dropdown filter"],
    "interview":["What is the difference between SELECT * and SELECT col1, col2?","Why should you avoid SELECT * in production queries?","Can you use a column alias in the WHERE clause? Why or why not?"],
    "tasks":["Write a query selecting employee name, department, and salary*12 as annual_salary","Use DISTINCT to find all unique cities in a customer table","Create a full_name column by concatenating first_name and last_name"],
    "mistakes":["Using SELECT * in production — transfers unnecessary data, breaks on schema changes","Trying to filter by alias in WHERE (aliases aren't available at WHERE stage)","Forgetting that SELECT executes AFTER FROM and WHERE"],
    "tips":["Always name your columns explicitly — makes code self-documenting","Use AS for every expression or calculation column","Ctrl+Enter in DBeaver to run selected query only"],
    "video":"https://www.youtube.com/results?search_query=SQL+SELECT+statement+tutorial+beginners"
  },
  { "name":"WHERE clause — filtering rows",
    "desc":"Filter rows before aggregation. The most-used clause after SELECT.",
    "level":"beg","must":True,
    "time":"1-2 hrs","order":2,
    "why":"Without WHERE, every query returns all rows. Real-world tables have millions of rows — filtering is how you get meaningful, fast results.",
    "concepts":["WHERE condition filters rows before GROUP BY","Cannot use SELECT aliases in WHERE (execution order)","Multiple conditions with AND / OR","Comparison: =, !=, <>, >, <, >=, <=","Pattern matching: LIKE '%keyword%', ILIKE for case-insensitive"],
    "keycode":["SELECT * FROM orders WHERE status = 'shipped' AND amount > 1000;","SELECT name FROM users WHERE email LIKE '%@gmail.com';","SELECT * FROM employees WHERE department != 'HR' AND salary >= 50000;"],
    "realworld":["Filter only active subscriptions from a billing table","Find customers who signed up in the last 30 days","Pull orders above a revenue threshold for a VIP report"],
    "interview":["What is the difference between WHERE and HAVING?","Why can't you use a GROUP BY alias in WHERE?","How do you filter rows where a date column is in the last 7 days?"],
    "tasks":["Write a query to find all orders with status='delivered' and amount > 500","Filter customers who registered after 2023-01-01 using WHERE","Find all employees NOT in the 'Sales' department"],
    "mistakes":["Using WHERE to filter aggregates — use HAVING instead","WHERE col = NULL instead of WHERE col IS NULL (never works!)","Forgetting AND/OR precedence — always use parentheses for complex logic"],
    "tips":["Put the most restrictive condition first for readability","Use BETWEEN for date ranges: WHERE date BETWEEN '2024-01-01' AND '2024-12-31'","ILIKE is PostgreSQL — use LOWER(col) LIKE '%term%' for portability"],
    "video":"https://www.youtube.com/results?search_query=SQL+WHERE+clause+tutorial"
  },
  { "name":"GROUP BY and aggregate functions (COUNT, SUM, AVG, MIN, MAX)",
    "desc":"Collapse rows into groups and compute metrics — the core of analytics SQL.",
    "level":"beg","must":True,
    "time":"2-3 hrs","order":3,
    "why":"GROUP BY is the SQL equivalent of Excel PivotTables. Every analytical report — sales by region, orders by month, users by country — uses this.",
    "concepts":["GROUP BY collapses rows to one per unique group value","Aggregate functions: COUNT(*), SUM(col), AVG(col), MIN(col), MAX(col)","COUNT(*) vs COUNT(col) vs COUNT(DISTINCT col)","Every non-aggregated SELECT column must be in GROUP BY","HAVING filters groups after aggregation"],
    "keycode":["SELECT department, COUNT(*) AS headcount, AVG(salary) AS avg_sal\nFROM employees GROUP BY department;","SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS revenue\nFROM orders GROUP BY 1 ORDER BY 1;","SELECT category, COUNT(DISTINCT user_id) AS buyers\nFROM orders GROUP BY category HAVING COUNT(*) > 100;"],
    "realworld":["Monthly revenue report by region and product category","Count unique customers per city for market sizing","Find departments with more than 10 employees (HAVING)"],
    "interview":["What is the difference between COUNT(*), COUNT(col), and COUNT(DISTINCT col)?","Why do you get an error when you SELECT a column not in GROUP BY?","Can you GROUP BY a calculated expression? Give an example."],
    "tasks":["Write a query: total orders and revenue by month for 2024","Count unique customers per city — only cities with 50+ customers","Find the top 5 products by total sales using GROUP BY + ORDER BY + LIMIT"],
    "mistakes":["Selecting columns not in GROUP BY (SQL error in strict mode)","Using COUNT(col) when you want COUNT(*) — misses the point","Forgetting HAVING for post-aggregation filters — using WHERE instead"],
    "tips":["GROUP BY 1, 2 is shorthand for the 1st and 2nd SELECT columns — use carefully","HAVING COUNT(*) > 1 is the classic duplicate-detection pattern","Round averages: ROUND(AVG(salary), 2) for readable output"],
    "video":"https://www.youtube.com/results?search_query=SQL+GROUP+BY+aggregate+functions+tutorial"
  },
  { "name":"CASE WHEN THEN ELSE END — conditional logic",
    "desc":"SQL's if-else. Works inside SELECT, GROUP BY, ORDER BY, and aggregate functions.",
    "level":"beg","must":True,
    "time":"2 hrs","order":4,
    "why":"CASE WHEN is used everywhere — customer segmentation, status labels, pivots, conditional aggregation. It appears in almost every real analytics query.",
    "concepts":["CASE WHEN cond THEN val ELSE default END","Can be nested: CASE WHEN ... THEN CASE WHEN ...","Used inside SUM/COUNT for conditional aggregation","Searched CASE vs simple CASE","CASE in GROUP BY to create custom buckets"],
    "keycode":["SELECT name,\n  CASE WHEN salary > 100000 THEN 'Senior'\n       WHEN salary > 60000 THEN 'Mid'\n       ELSE 'Junior' END AS level\nFROM employees;","SELECT SUM(CASE WHEN status='paid' THEN amount ELSE 0 END) AS paid_revenue\nFROM invoices;","SELECT CASE WHEN age < 25 THEN '18-24'\n            WHEN age < 35 THEN '25-34'\n            ELSE '35+' END AS age_band, COUNT(*)\nFROM users GROUP BY 1;"],
    "realworld":["Segment customers into tiers based on spend","Pivot: show paid vs unpaid revenue in one row","Create age bands for demographic reporting"],
    "interview":["How do you create a pivot table in SQL using CASE WHEN?","What is the difference between a searched CASE and a simple CASE?","How do you use CASE WHEN inside an aggregate function?"],
    "tasks":["Write a query labeling orders as 'Large' (>1000), 'Medium' (>200), or 'Small'","Use CASE inside SUM to calculate revenue from only 'completed' orders","Create a customer tier column: Platinum/Gold/Silver/Bronze based on total spend"],
    "mistakes":["Forgetting the END keyword at the close of CASE","Not providing an ELSE clause — returns NULL for unmatched rows","Using CASE WHEN where COALESCE would be simpler for NULL replacement"],
    "tips":["CASE WHEN in GROUP BY creates custom buckets without changing the raw data","SUM(CASE WHEN condition THEN 1 ELSE 0 END) counts matching rows — faster than a subquery","Always include an ELSE to handle unexpected values"],
    "video":"https://www.youtube.com/results?search_query=SQL+CASE+WHEN+tutorial+analytics"
  },
  { "name":"NULL handling: IS NULL, IS NOT NULL, COALESCE, NULLIF",
    "desc":"NULLs are the silent killer of wrong analytics. Master NULL behavior early.",
    "level":"beg","must":True,
    "time":"1.5 hrs","order":5,
    "why":"NULL in SQL is not zero, not empty string — it means unknown. Arithmetic with NULL returns NULL. Comparisons with NULL return NULL. This trips up almost every beginner.",
    "concepts":["NULL = NULL is false — always use IS NULL / IS NOT NULL","Any arithmetic with NULL returns NULL (5 + NULL = NULL)","COALESCE(col, default) returns first non-NULL value","NULLIF(a, b) returns NULL if a equals b — prevents divide-by-zero","COUNT(*) counts all rows; COUNT(col) excludes NULLs"],
    "keycode":["SELECT * FROM orders WHERE discount IS NOT NULL;","SELECT COALESCE(phone, 'No Phone') AS contact FROM customers;","SELECT revenue / NULLIF(units, 0) AS avg_price FROM products;","SELECT COUNT(*) AS all_rows, COUNT(email) AS with_email FROM users;"],
    "realworld":["Replace NULL payment methods with 'Unknown' in a report","Avoid divide-by-zero in unit price calculations","Find customers with no assigned sales rep (manager_id IS NULL)"],
    "interview":["What is the difference between NULL and an empty string in SQL?","How does NULL behave in aggregate functions?","How do you prevent divide-by-zero errors in SQL?"],
    "tasks":["Find all orders where the discount column is NULL","Use COALESCE to replace NULL shipping addresses with 'Not Provided'","Calculate average order value using NULLIF to handle zero-unit orders"],
    "mistakes":["WHERE col = NULL (always returns nothing — must use IS NULL)","Assuming COUNT(*) and COUNT(col) are the same","Not handling NULLs in JOINs — can cause unexpected row drops"],
    "tips":["COALESCE accepts multiple arguments — first non-null wins","Use NULLIF in denominators to prevent division-by-zero gracefully","NULL in ORDER BY: use NULLS FIRST or NULLS LAST explicitly"],
    "video":"https://www.youtube.com/results?search_query=SQL+NULL+handling+COALESCE+tutorial"
  },
  { "name":"JOINs: INNER, LEFT, RIGHT, FULL OUTER",
    "desc":"Combine data from multiple tables — the most important concept after SELECT.",
    "level":"beg","must":True,
    "time":"3-4 hrs","order":6,
    "why":"Real data always lives in multiple tables. Every analyst report combines at least 2 tables. JOINs are tested in every SQL interview without exception.",
    "concepts":["INNER JOIN: only matching rows in both tables","LEFT JOIN: all left + matched right (NULL where no match)","RIGHT JOIN: all right + matched left (rarely used)","FULL OUTER JOIN: all rows from both, NULLs where no match","Anti-JOIN: LEFT JOIN + WHERE right.id IS NULL"],
    "keycode":["SELECT o.order_id, u.name, o.amount\nFROM orders o\nINNER JOIN users u ON o.user_id = u.id;","-- Find users with NO orders (anti-join)\nSELECT u.name FROM users u\nLEFT JOIN orders o ON u.id = o.user_id\nWHERE o.user_id IS NULL;","SELECT o.*, p.product_name, c.category_name\nFROM orders o\nJOIN products p ON o.product_id = p.id\nJOIN categories c ON p.category_id = c.id;"],
    "realworld":["Add customer name to every order (INNER JOIN)","Find customers who haven't ordered yet (LEFT anti-join)","Build a sales report combining orders + products + categories"],
    "interview":["What is the difference between INNER JOIN and LEFT JOIN?","How do you find records in Table A that have no match in Table B?","What happens to row count when you JOIN on a non-unique key?"],
    "tasks":["Join orders to users and products — show order details with names","Use LEFT JOIN to find all products that have never been ordered","Check for JOIN duplicates: verify row count before and after"],
    "mistakes":["Not checking for duplicate keys before joining — silently multiplies rows","Using RIGHT JOIN instead of reordering to LEFT JOIN (confusing to read)","Joining on columns with different data types — implicit cast kills index performance"],
    "tips":["Always alias tables (o, u, p) in multi-table queries","After every JOIN, check: SELECT COUNT(*) — did rows multiply unexpectedly?","Anti-JOIN pattern (LEFT + WHERE IS NULL) is faster than NOT IN with NULLs"],
    "video":"https://www.youtube.com/results?search_query=SQL+JOINs+tutorial+INNER+LEFT+JOIN+explained"
  },
  { "name":"Subqueries and CTEs (WITH clause)",
    "desc":"Write SQL within SQL. CTEs make complex multi-step logic readable.",
    "level":"int","must":True,
    "time":"3 hrs","order":7,
    "why":"Real analytics queries have multiple steps. Subqueries and CTEs let you build logic incrementally. CTEs are the professional standard — every senior analyst uses them daily.",
    "concepts":["Subquery in WHERE: WHERE user_id IN (SELECT ...)","Subquery in FROM: derived table","Correlated subquery: references outer query (slow — avoid if possible)","CTE: WITH name AS (...) SELECT ... FROM name","Multiple CTEs: WITH a AS (...), b AS (...) SELECT ... FROM a JOIN b"],
    "keycode":["-- CTE: clean, readable, debuggable\nWITH active_users AS (\n  SELECT id FROM users WHERE status = 'active'\n),\nrecent_orders AS (\n  SELECT user_id, SUM(amount) AS total\n  FROM orders WHERE order_date >= '2024-01-01'\n  GROUP BY user_id\n)\nSELECT u.id, r.total\nFROM active_users u\nJOIN recent_orders r ON u.id = r.user_id;"],
    "realworld":["Calculate revenue only for active users (subquery in WHERE)","Multi-step report: first aggregate, then rank, then filter top 10","Deduplication: keep only the latest record per user"],
    "interview":["What is the difference between a CTE and a subquery?","When would you use a temp table instead of a CTE?","What is a correlated subquery and why can it be slow?"],
    "tasks":["Rewrite a nested subquery as a CTE — compare readability","Write a CTE to find top 5 customers by revenue, then show their order details","Use a subquery in WHERE to filter orders for premium users only"],
    "mistakes":["Deeply nesting subqueries — unreadable and unmaintainable","Referencing a CTE name more than once in heavy queries (re-computed each time in most DBs)","Using correlated subqueries on large tables — O(n) re-execution"],
    "tips":["Name CTEs after what they represent: active_users, monthly_cohorts","CTEs are not always materialized — use temp tables for expensive intermediate results","Build complex queries CTE by CTE: test each step before adding the next"],
    "video":"https://www.youtube.com/results?search_query=SQL+CTE+WITH+clause+subquery+tutorial"
  },
  { "name":"Window Functions: ROW_NUMBER, RANK, LAG, SUM OVER",
    "desc":"Perform calculations across rows without collapsing them — the most powerful SQL feature for analytics.",
    "level":"adv","must":True,
    "time":"4-5 hrs","order":8,
    "why":"Window functions are what separate intermediate from advanced SQL analysts. They appear in every hard SQL interview and are used daily for ranking, period-over-period, running totals, and moving averages.",
    "concepts":["OVER() clause defines the window — no rows collapsed","PARTITION BY: groups (like GROUP BY but keeps rows)","ORDER BY inside OVER: defines ordering within window","ROW_NUMBER: unique rank. RANK: ties+gap. DENSE_RANK: ties no gap","LAG/LEAD: previous/next row. SUM OVER: running total. AVG OVER: moving avg","NTILE(n): divide into n equal buckets","Window frame: ROWS BETWEEN N PRECEDING AND CURRENT ROW"],
    "keycode":["-- Top customer per region\nSELECT region, customer_id, revenue,\n  DENSE_RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS rank\nFROM orders;","-- Month-over-month revenue change\nSELECT month, revenue,\n  LAG(revenue,1) OVER (ORDER BY month) AS prev_month,\n  revenue - LAG(revenue,1) OVER (ORDER BY month) AS change\nFROM monthly_revenue;","-- 7-day moving average\nSELECT date, revenue,\n  AVG(revenue) OVER (ORDER BY date\n    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7d\nFROM daily_sales;"],
    "realworld":["Rank top 3 salespeople in each region without separate queries","Calculate month-over-month revenue change for every product","Running total of cumulative revenue for a fiscal year","Customer quartile segmentation for marketing tiers"],
    "interview":["What is the difference between ROW_NUMBER, RANK, and DENSE_RANK?","How do you calculate a 7-day moving average using SQL?","What is the difference between PARTITION BY and GROUP BY?","How do you get the previous month's revenue for every row?"],
    "tasks":["Find the top 3 products by sales in each category using DENSE_RANK","Calculate week-over-week order count change using LAG","Build a running total of revenue column ordered by date","Assign customers to quartiles by spend using NTILE(4)"],
    "mistakes":["Confusing PARTITION BY (keeps rows) with GROUP BY (collapses rows)","Using RANK when DENSE_RANK is needed — gaps in top-N queries","Forgetting ROWS BETWEEN in moving averages — default RANGE frame can give wrong results"],
    "tips":["Window functions run AFTER GROUP BY — you can combine them","ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW = running total","Practice: write every window function example on a sample 5-row table first"],
    "video":"https://www.youtube.com/results?search_query=SQL+window+functions+tutorial+ROW_NUMBER+LAG+RANK"
  },
  { "name":"Date Functions: DATE_TRUNC, DATEDIFF, EXTRACT, date arithmetic",
    "desc":"Manipulate and group dates — essential for every time-series and cohort analysis.",
    "level":"beg","must":True,
    "time":"2 hrs","order":9,
    "why":"Almost every analytics report is time-based. Monthly trends, cohort analysis, age calculations, date filtering — all require mastery of date functions.",
    "concepts":["DATE_TRUNC('month', ts): truncates to first of month","EXTRACT(year FROM date): pulls year/month/day/DOW","DATEDIFF(unit, start, end): integer difference between dates","DATE_ADD / INTERVAL arithmetic: date + INTERVAL '30 days'","CURRENT_DATE, NOW(), GETDATE() — current timestamp functions","Functions differ by DB: PostgreSQL vs MySQL vs Snowflake vs BigQuery"],
    "keycode":["-- Group by month\nSELECT DATE_TRUNC('month', order_date) AS month,\n  SUM(amount) AS revenue\nFROM orders GROUP BY 1 ORDER BY 1;","-- Days since event\nSELECT user_id,\n  CURRENT_DATE - last_login::date AS days_inactive\nFROM users;","-- Last 30 days filter\nSELECT * FROM orders\nWHERE order_date >= CURRENT_DATE - INTERVAL '30 days';"],
    "realworld":["Monthly/weekly revenue trend reports","Customer recency: days since last purchase","Filter to current month or last quarter data","Employee tenure calculation in years and months"],
    "interview":["How do you group transactions by month in SQL?","How do you calculate the number of days between two dates?","How do you filter the last 30 days dynamically (without hardcoding a date)?"],
    "tasks":["Write a query showing monthly order count and revenue for 2024","Calculate days since each customer's last purchase","Find all users who haven't logged in for more than 90 days"],
    "mistakes":["Hardcoding dates — use CURRENT_DATE - INTERVAL instead","DATE_TRUNC returns the start of the period (midnight, Jan 1 of month)","DATEDIFF syntax differs across databases — always check your dialect"],
    "tips":["DATE_TRUNC is your best friend for time-series grouping","Use EXTRACT(DOW FROM date) for day-of-week analysis (0=Sunday in PostgreSQL)","TO_CHAR(date, 'YYYY-MM') in PostgreSQL for readable month labels"],
    "video":"https://www.youtube.com/results?search_query=SQL+date+functions+DATE_TRUNC+DATEDIFF+tutorial"
  },
  { "name":"HAVING clause — filtering aggregated groups",
    "desc":"Filter the results of GROUP BY. You cannot use aggregate functions in WHERE.",
    "level":"beg","must":True,
    "time":"1 hr","order":10,
    "why":"HAVING is one of the most commonly confused concepts in SQL interviews. Understanding when to use WHERE vs HAVING demonstrates real SQL competence.",
    "concepts":["HAVING filters AFTER GROUP BY; WHERE filters BEFORE","HAVING can use aggregate functions (WHERE cannot)","HAVING without GROUP BY filters the entire table as one group","Execution order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY"],
    "keycode":["-- Only departments with 5+ employees\nSELECT department, COUNT(*) AS headcount\nFROM employees\nGROUP BY department\nHAVING COUNT(*) >= 5;","-- Customers who spent more than 10,000 total\nSELECT customer_id, SUM(amount) AS total_spend\nFROM orders\nGROUP BY customer_id\nHAVING SUM(amount) > 10000;"],
    "realworld":["Find product categories with more than 100 orders","Identify customers who ordered more than 5 times in a month","Filter cities with average order value above a threshold"],
    "interview":["What is the difference between WHERE and HAVING?","Can you use HAVING without GROUP BY? What does it do?","In what order does SQL execute WHERE vs GROUP BY vs HAVING?"],
    "tasks":["Find all products with total sales > 100 units using HAVING","Find categories where average order value > 500 AND order count > 50","Rewrite a query that incorrectly uses WHERE on an aggregate — fix with HAVING"],
    "mistakes":["Using WHERE to filter aggregates — SQL error","Using HAVING to filter individual rows — works but WHERE is faster","Forgetting that HAVING uses aggregate expressions, not aliases"],
    "tips":["You can use both WHERE and HAVING in the same query — they filter at different stages","HAVING COUNT(*) > 1 is the classic duplicate detection pattern","Think: WHERE = filter rows, HAVING = filter groups"],
    "video":"https://www.youtube.com/results?search_query=SQL+HAVING+clause+vs+WHERE+tutorial"
  },
]

SQL_INTERMEDIATE = [
  { "name":"INNER JOIN — matching rows in both tables",
    "desc":"The most common JOIN. Returns rows where the join condition matches in both tables.",
    "level":"int","must":True,
    "time":"2 hrs","order":1,
    "why":"INNER JOIN is the default way to combine related tables. If you can't write accurate INNER JOINs quickly, you can't do analytics SQL.",
    "concepts":["Returns only rows with a match in both tables","Non-matching rows are completely excluded","Multiple join conditions: ON a.id = b.id AND a.type = b.type","Implicit INNER JOIN (comma syntax) — avoid, use explicit JOIN","Equi-join vs non-equi join (joining on ranges or expressions)"],
    "keycode":["SELECT o.order_id, u.name, u.email, o.amount\nFROM orders o\nINNER JOIN users u ON o.user_id = u.id\nWHERE o.status = 'completed';","-- Multi-table INNER JOIN\nSELECT o.id, p.name, c.category_name, o.quantity\nFROM orders o\nJOIN products p ON o.product_id = p.id\nJOIN categories c ON p.category_id = c.id;"],
    "realworld":["Add customer name and email to every order for reporting","Combine product, category, and supplier info for a catalog report","Build a transaction report joining orders, users, and payment tables"],
    "interview":["What rows does INNER JOIN exclude vs LEFT JOIN?","What happens to row count when you INNER JOIN on a column with duplicates?","Write an INNER JOIN to get employees with their manager's name."],
    "tasks":["Join the orders table to users — add name and city to each order","3-table join: orders + products + suppliers — show full order details","Verify row count before and after — did any rows get dropped?"],
    "mistakes":["Not aliasing tables — queries become unreadable with 3+ tables","Joining on wrong column — check foreign key relationships first","Not realizing INNER JOIN drops rows with no match — use LEFT if you need all rows"],
    "tips":["Always check: is this join one-to-many? Does that affect my aggregations?","Use table aliases (o, u, p) consistently — first letter of table name","Test JOINs on 5-row sample data before running on millions of rows"],
    "video":"https://www.youtube.com/results?search_query=SQL+INNER+JOIN+tutorial+explained"
  },
  { "name":"LEFT JOIN and anti-JOIN patterns",
    "desc":"Keep all rows from the left table regardless of whether a match exists in the right.",
    "level":"int","must":True,
    "time":"2 hrs","order":2,
    "why":"LEFT JOIN is the most important JOIN in analytics. Finding 'users with no orders', 'products never sold', 'dates with no events' — all use LEFT JOIN anti-join pattern.",
    "concepts":["LEFT JOIN: all left rows + matched right (NULL where no match)","Anti-JOIN: LEFT JOIN + WHERE right_key IS NULL","Diagnosing LEFT JOIN: NULL columns from right table signal no match","LEFT JOIN changes to INNER JOIN silently if you WHERE filter on right table columns","Multiple LEFT JOINs are fine — order and aliasing matter"],
    "keycode":["-- Users who have NEVER placed an order\nSELECT u.id, u.name\nFROM users u\nLEFT JOIN orders o ON u.id = o.user_id\nWHERE o.user_id IS NULL;","-- All products with their total sales (0 if never sold)\nSELECT p.name, COALESCE(SUM(o.amount), 0) AS total_sales\nFROM products p\nLEFT JOIN orders o ON p.id = o.product_id\nGROUP BY p.id, p.name;"],
    "realworld":["Find churned customers (signed up but no purchase in 90 days)","All dates in a calendar with 0 revenue on slow days","Products that have never been sold — inventory cleanup"],
    "interview":["What is an anti-JOIN and how do you write one?","If you add a WHERE clause on the right table of a LEFT JOIN, what does it become?","Why does COALESCE matter after LEFT JOIN?"],
    "tasks":["Find all customers who have never made a purchase","Show every product with its total sold quantity — 0 for unsold products","Find users who registered in January but never completed their profile"],
    "mistakes":["Adding WHERE on right-table column — turns LEFT JOIN into INNER JOIN","Forgetting COALESCE for the aggregated column — NULL instead of 0","Confusing which table is 'left' — it's the one in FROM, not the one that's 'more important'"],
    "tips":["Anti-JOIN is faster than NOT IN when NULLs exist in the right table","After LEFT JOIN + GROUP BY: use COALESCE(SUM(col), 0) for clean zeros","Draw a Venn diagram mentally before writing any JOIN"],
    "video":"https://www.youtube.com/results?search_query=SQL+LEFT+JOIN+anti+join+tutorial"
  },
  { "name":"CTEs: WITH clause — multi-step query logic",
    "desc":"Named temporary result sets that make complex multi-step SQL readable and maintainable.",
    "level":"int","must":True,
    "time":"3 hrs","order":3,
    "why":"CTEs are the professional standard for complex analytics SQL. They replace nested subqueries with readable, named steps. Every senior analyst writes CTE-first.",
    "concepts":["WITH name AS (query) SELECT ... FROM name","Multiple CTEs: WITH a AS (...), b AS (...) — b can reference a","CTEs improve readability but are usually not materialized (re-computed if used multiple times)","Recursive CTEs: with RECURSIVE keyword for hierarchies and date sequences","Naming matters: name CTEs after what they represent"],
    "keycode":["WITH monthly_revenue AS (\n  SELECT DATE_TRUNC('month', order_date) AS month,\n         SUM(amount) AS revenue\n  FROM orders GROUP BY 1\n),\nranked AS (\n  SELECT *, RANK() OVER (ORDER BY revenue DESC) AS rank\n  FROM monthly_revenue\n)\nSELECT * FROM ranked WHERE rank <= 3;"],
    "realworld":["Multi-step cohort analysis: first get cohorts, then activity, then retention","Deduplication: CTE to find duplicates, then outer query to delete","Build complex reports step-by-step without nested hell"],
    "interview":["What is the difference between a CTE and a subquery in terms of readability and performance?","When would you use a temporary table instead of a CTE?","Can a CTE reference itself? What is that called?"],
    "tasks":["Rewrite a 3-level nested subquery using CTEs","Build a 3-step CTE: filter active users → calculate their spend → rank them","Write a recursive CTE to generate a sequence of 30 dates"],
    "mistakes":["Re-using a CTE name multiple times — may be recomputed (use temp table instead)","Building a 10-step CTE chain without testing each step individually","Using CTEs where a simple JOIN would suffice — over-engineering"],
    "tips":["Test each CTE individually: SELECT * FROM cte_name LIMIT 10 during development","Name CTEs like sentences: active_paid_users, monthly_cohort_counts","In Snowflake, BigQuery — CTEs are often materialized automatically for repeated use"],
    "video":"https://www.youtube.com/results?search_query=SQL+CTE+WITH+clause+advanced+tutorial"
  },
  { "name":"UNION, UNION ALL, INTERSECT, EXCEPT — combining result sets",
    "desc":"Stack multiple query results vertically. UNION ALL is the performance-safe default.",
    "level":"int","must":False,
    "time":"1.5 hrs","order":4,
    "why":"Combining results from multiple tables (e.g., web + app orders, current + historical data) is a common ETL and reporting task. UNION ALL is in almost every data pipeline.",
    "concepts":["UNION ALL: keeps ALL rows including duplicates (fast, O(n))","UNION: removes duplicates (slow — sorts entire result)","Column count and data types must match across queries","INTERSECT: rows present in both queries","EXCEPT (MINUS in Oracle): rows in first but not in second","Column names taken from first SELECT"],
    "keycode":["-- Combine web and app orders\nSELECT order_id, user_id, amount, 'web' AS source FROM web_orders\nUNION ALL\nSELECT order_id, user_id, amount, 'app' AS source FROM app_orders;","-- Find products that exist in both old and new catalog\nSELECT product_code FROM catalog_2023\nINTERSECT\nSELECT product_code FROM catalog_2024;"],
    "realworld":["Combine transaction data from multiple regional databases","Stack current month with historical archive","Find customers who exist in both CRM and billing systems"],
    "interview":["What is the difference between UNION and UNION ALL? When would you use each?","How do you combine three tables with different column names using UNION ALL?","What does EXCEPT do? Give a real-world example."],
    "tasks":["Combine orders from two regional tables with UNION ALL — add a 'region' label column","Find product IDs present in inventory_2023 but NOT in inventory_2024 using EXCEPT","Verify UNION removes duplicates vs UNION ALL by counting rows"],
    "mistakes":["Using UNION when UNION ALL is sufficient — unnecessary sort+dedup overhead","Column count mismatch between queries (SQL error)","Assuming column names match — they come from the FIRST SELECT statement"],
    "tips":["Default to UNION ALL — only use UNION when deduplication is genuinely required","Add a source label column: 'web' AS source so you can distinguish after union","ORDER BY goes at the very end, applies to the entire combined result"],
    "video":"https://www.youtube.com/results?search_query=SQL+UNION+UNION+ALL+INTERSECT+tutorial"
  },
  { "name":"Indexes and query performance basics",
    "desc":"Understand how indexes work and how to write queries that actually use them.",
    "level":"int","must":False,
    "time":"2.5 hrs","order":5,
    "why":"As a data analyst, you will face slow queries. Understanding indexes helps you write queries that run in seconds instead of minutes on large production tables.",
    "concepts":["Index = sorted B-tree pointer structure on a column","WHERE and JOIN columns should be indexed for fast lookups","Composite index: index on (col_a, col_b) — column order matters","Functions on indexed columns kill the index: WHERE YEAR(date) = 2024 (bad)","EXPLAIN / EXPLAIN ANALYZE shows if index is used — look for Seq Scan vs Index Scan","Covering index: includes all columns needed — avoids table lookup"],
    "keycode":["-- This KILLS the index on order_date:\nWHERE YEAR(order_date) = 2024\n\n-- This USES the index:\nWHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';","-- Check query plan in PostgreSQL\nEXPLAIN ANALYZE\nSELECT * FROM orders WHERE user_id = 12345 AND status = 'paid';"],
    "realworld":["Query on 10M-row orders table takes 30s — adding an index makes it 200ms","Understanding why a WHERE filter on a function-wrapped column is slow","Reading EXPLAIN output to diagnose performance in production"],
    "interview":["What is an index in a database and how does it speed up queries?","Why does using a function on an indexed column prevent index usage?","What does EXPLAIN ANALYZE show you?"],
    "tasks":["Run EXPLAIN ANALYZE on a slow query — identify if indexes are being used","Rewrite a function-based WHERE filter to use the index properly","Compare query time: filtered on indexed vs non-indexed column"],
    "mistakes":["Wrapping indexed columns in functions in WHERE (breaks index usage)","Adding indexes on every column — indexes slow down INSERTs/UPDATEs","Not running EXPLAIN ANALYZE to verify performance assumptions"],
    "tips":["The golden rule: don't transform the column in WHERE — transform the literal instead","INDEX on (user_id, status) serves queries filtering both; order matters","Ask your DBA before creating indexes in production — they have storage and write cost"],
    "video":"https://www.youtube.com/results?search_query=SQL+indexes+query+performance+tutorial+explained"
  },
  { "name":"Pivot patterns with CASE WHEN — reshape rows to columns",
    "desc":"Transform row-level values into columns — the SQL version of Excel's pivot table.",
    "level":"int","must":True,
    "time":"2 hrs","order":6,
    "why":"Business reports almost always require wide-format: months as columns, categories as columns. SQL's CASE WHEN pivot is how you build these without exporting to Excel.",
    "concepts":["Conditional aggregation: SUM(CASE WHEN col='A' THEN value END) AS col_a","One CASE block per pivot column","Works in any SQL database (no PIVOT keyword needed)","Snowflake/SQL Server have native PIVOT syntax","Dynamic pivot requires dynamic SQL (advanced)"],
    "keycode":["SELECT\n  product_id,\n  SUM(CASE WHEN month = 'Jan' THEN revenue END) AS jan,\n  SUM(CASE WHEN month = 'Feb' THEN revenue END) AS feb,\n  SUM(CASE WHEN month = 'Mar' THEN revenue END) AS mar\nFROM monthly_sales\nGROUP BY product_id;","-- Count by status in one row\nSELECT\n  COUNT(CASE WHEN status='active' THEN 1 END) AS active,\n  COUNT(CASE WHEN status='churned' THEN 1 END) AS churned,\n  COUNT(CASE WHEN status='trial' THEN 1 END) AS trial\nFROM users;"],
    "realworld":["Monthly revenue by product as a matrix report","Count users in each status in a single summary row","Cross-tabulation of category × region for a heatmap"],
    "interview":["How do you create a pivot table in SQL?","What is conditional aggregation and how does it differ from a regular GROUP BY?","How would you show Q1/Q2/Q3/Q4 revenue as separate columns?"],
    "tasks":["Write a pivot showing Jan-Jun revenue per product as columns","Create a status breakdown: one row per department with active/inactive/pending counts","Build a region × channel revenue matrix using CASE WHEN"],
    "mistakes":["Forgetting GROUP BY on the row dimension","Using WHERE to filter inside pivot instead of CASE WHEN — loses other rows","Not using SUM — COUNT or MAX also works depending on the data"],
    "tips":["Snowflake PIVOT syntax is cleaner — learn it if you use Snowflake","Add a TOTAL column using regular SUM(revenue) alongside the pivoted columns","Always add ELSE 0 or ELSE NULL to make intent explicit"],
    "video":"https://www.youtube.com/results?search_query=SQL+pivot+CASE+WHEN+tutorial"
  },
]

SQL_ADVANCED = [
  { "name":"Window functions deep dive: PARTITION BY, frames, NTILE",
    "desc":"Advanced window function patterns for real analytics work.",
    "level":"adv","must":True,
    "time":"4 hrs","order":1,
    "why":"Advanced window function patterns appear in every senior analyst interview and are used daily at product companies for ranking, moving averages, and cohort analysis.",
    "concepts":["PARTITION BY: restart calculation for each group","ORDER BY inside OVER: defines sort order within window","Window frame: ROWS BETWEEN vs RANGE BETWEEN","UNBOUNDED PRECEDING = first row of partition; CURRENT ROW = this row","NTILE(n): divide rows into n equal groups (quartiles, deciles)","FIRST_VALUE, LAST_VALUE: first/last in window","PERCENT_RANK, CUME_DIST: relative position 0-1"],
    "keycode":["-- Percentile bucket customers into 4 value tiers\nSELECT customer_id, total_spend,\n  NTILE(4) OVER (ORDER BY total_spend DESC) AS quartile\nFROM customer_summary;","-- Running total by region\nSELECT region, month, revenue,\n  SUM(revenue) OVER (\n    PARTITION BY region\n    ORDER BY month\n    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n  ) AS cumulative_revenue\nFROM monthly_sales;","-- 30-day moving average\nSELECT date, revenue,\n  AVG(revenue) OVER (\n    ORDER BY date\n    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW\n  ) AS ma_30d\nFROM daily_revenue;"],
    "realworld":["Segment customers into value tiers for targeted marketing","Cumulative revenue chart for investor reporting","30-day rolling average to smooth daily noise in dashboards"],
    "interview":["What is the difference between ROWS BETWEEN and RANGE BETWEEN?","How do you calculate a 30-day moving average using a window function?","How do you assign customers to quartiles? What function do you use?"],
    "tasks":["Segment customers into deciles by lifetime value using NTILE(10)","Calculate cumulative revenue per region ordered by month","Find the running maximum price per product category over time"],
    "mistakes":["LAST_VALUE without explicit frame returns wrong result — needs ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING","Mixing GROUP BY and window functions without understanding execution order","Forgetting PARTITION BY where the calculation should restart per group"],
    "tips":["Window functions run AFTER GROUP BY — you can window on aggregated results","ROWS BETWEEN is almost always safer than RANGE for time-series","Alias window: OVER w WHERE w is defined in WINDOW clause — cleaner for repeated windows"],
    "video":"https://www.youtube.com/results?search_query=SQL+advanced+window+functions+PARTITION+BY+tutorial"
  },
  { "name":"Cohort analysis SQL pattern — end-to-end",
    "desc":"The most important analytics SQL pattern: track user behavior over time by acquisition cohort.",
    "level":"adv","must":True,
    "time":"5 hrs","order":2,
    "why":"Cohort analysis is asked in almost every senior data analyst interview at product companies. It's used weekly at Flipkart, Zomato, Swiggy, PhonePe — any company with returning users.",
    "concepts":["Cohort = group of users who share a characteristic (usually first purchase month)","Retention = % of cohort still active in each subsequent period","Step 1: find cohort month (MIN order date per user)","Step 2: join back to all activity","Step 3: calculate period index (months since cohort)","Step 4: pivot to matrix format","Absolute retention (count) vs relative (%)"],
    "keycode":["WITH cohorts AS (\n  SELECT user_id,\n    DATE_TRUNC('month', MIN(order_date)) AS cohort_month\n  FROM orders GROUP BY 1\n),\nactivity AS (\n  SELECT o.user_id, c.cohort_month,\n    DATEDIFF('month', c.cohort_month, o.order_date) AS period\n  FROM orders o JOIN cohorts c ON o.user_id = c.user_id\n),\ncohort_sizes AS (\n  SELECT cohort_month, COUNT(DISTINCT user_id) AS cohort_size\n  FROM cohorts GROUP BY 1\n)\nSELECT a.cohort_month, a.period,\n  COUNT(DISTINCT a.user_id) AS retained,\n  ROUND(100.0 * COUNT(DISTINCT a.user_id) / cs.cohort_size, 1) AS retention_pct\nFROM activity a\nJOIN cohort_sizes cs ON a.cohort_month = cs.cohort_month\nGROUP BY 1, 2\nORDER BY 1, 2;"],
    "realworld":["Monthly retention heatmap for product team — shows if product quality is improving","Cohort LTV comparison — which acquisition month brought best long-term customers","Identify the period where most users drop off — focus product investment there"],
    "interview":["Write a cohort retention query from scratch — this is asked at Amazon, Flipkart, Swiggy","How do you calculate the size of each cohort?","What does 'period 0' mean in a cohort analysis?"],
    "tasks":["Write the full cohort retention query on the UCI e-commerce dataset","Add a % of cohort column to show relative retention","Identify which cohort has the highest 3-month retention"],
    "mistakes":["Using order count instead of user count for retention — different metrics","Not handling users who appear in multiple cohorts (use MIN date, not all dates)","Forgetting period 0 — the cohort month itself (should be 100% by definition)"],
    "tips":["Always verify: period 0 retention should be exactly 100%","The query is the same pattern every time — memorize it, parameterize it","In Python: pd.crosstab + seaborn heatmap gives the visual — pair with this SQL"],
    "video":"https://www.youtube.com/results?search_query=SQL+cohort+retention+analysis+tutorial"
  },
  { "name":"Funnel analysis in SQL — conversion at each step",
    "desc":"Measure how users progress through a sequence of events and find where they drop off.",
    "level":"adv","must":True,
    "time":"3 hrs","order":3,
    "why":"Funnel analysis is a core product analytics technique. E-commerce (view→cart→checkout→purchase), marketing (impression→click→sign-up→activation), onboarding — every product team needs funnels.",
    "concepts":["User-level flags: MAX(CASE WHEN event='X' THEN 1 ELSE 0 END)","Sum flags for step counts","Conversion rate = step_n / step_1 * 100","Ordered funnel: user must complete steps in sequence (harder — use window functions)","Time-bounded funnel: only count conversions within N hours of first step"],
    "keycode":["WITH funnel AS (\n  SELECT user_id,\n    MAX(CASE WHEN event='product_view' THEN 1 ELSE 0 END) AS viewed,\n    MAX(CASE WHEN event='add_to_cart' THEN 1 ELSE 0 END) AS carted,\n    MAX(CASE WHEN event='checkout' THEN 1 ELSE 0 END) AS checkout,\n    MAX(CASE WHEN event='purchase' THEN 1 ELSE 0 END) AS purchased\n  FROM events WHERE date >= CURRENT_DATE - 30\n  GROUP BY 1\n)\nSELECT\n  SUM(viewed) AS step1_views,\n  SUM(carted) AS step2_cart,\n  ROUND(100.0 * SUM(carted) / NULLIF(SUM(viewed),0), 1) AS view_to_cart_pct,\n  SUM(checkout) AS step3_checkout,\n  SUM(purchased) AS step4_purchase,\n  ROUND(100.0 * SUM(purchased) / NULLIF(SUM(viewed),0), 1) AS overall_cvr\nFROM funnel;"],
    "realworld":["E-commerce checkout conversion funnel","Marketing campaign: impression → click → sign-up → first purchase","Onboarding funnel: registration → email verify → profile complete → first action"],
    "interview":["Write a funnel analysis query for a 4-step checkout process","How do you add conversion rates between each step?","How do you segment funnel results by device type?"],
    "tasks":["Build a 4-step checkout funnel for the last 30 days","Add device-level segmentation to the funnel (GROUP BY device_type)","Identify which step has the biggest drop-off"],
    "mistakes":["Counting all events instead of unique users — inflates funnel numbers","Not using NULLIF in the conversion rate denominator — divide-by-zero error","Unordered funnel counts users who completed step 3 before step 1 — flag if ordering matters"],
    "tips":["The MAX(CASE WHEN) pattern is the standard — memorize it","Add WHERE date >= CURRENT_DATE - 30 — always time-bound funnels","Segment every funnel by device, region, acquisition channel to find actionable insights"],
    "video":"https://www.youtube.com/results?search_query=SQL+funnel+analysis+tutorial+product+analytics"
  },
  { "name":"Query optimization — writing fast production SQL",
    "desc":"Techniques to diagnose and fix slow queries on large tables in production environments.",
    "level":"adv","must":False,
    "time":"3 hrs","order":4,
    "why":"As a data analyst you will write queries on tables with 100M+ rows. A query that takes 5 minutes can be rewritten to run in 5 seconds. This skill gets you promoted.",
    "concepts":["Never SELECT * on large tables — specify columns","Filter early: reduce rows before joining","Avoid functions on indexed WHERE columns (YEAR(date) breaks index)","Use EXPLAIN ANALYZE to see actual vs estimated row counts","Avoid DISTINCT on large results — find root cause of duplicates instead","Materialized views for expensive dashboards","Partition pruning: WHERE on partitioned column dramatically speeds queries"],
    "keycode":["-- BAD: Full scan, function on indexed column\nSELECT * FROM orders WHERE YEAR(order_date) = 2024;\n\n-- GOOD: Index range scan\nSELECT order_id, user_id, amount\nFROM orders\nWHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';","-- Check query plan\nEXPLAIN ANALYZE\nSELECT user_id, COUNT(*) FROM orders\nWHERE status = 'completed'\nGROUP BY user_id;"],
    "realworld":["Dashboard query taking 3 minutes reduced to 8 seconds with proper filtering","Identifying a missing index on a JOIN column that's causing full table scans","Refactoring a SELECT * + DISTINCT antipattern to a targeted column query"],
    "interview":["How would you diagnose a slow SQL query?","What are volatile functions and how do they affect query performance?","What is partition pruning and why does it matter?"],
    "tasks":["Take a slow query and rewrite it with proper column selection and early filtering","Use EXPLAIN ANALYZE to find a sequential scan — add appropriate index","Replace a correlated subquery with a window function and compare performance"],
    "mistakes":["SELECT * on tables with 50+ columns — massive I/O overhead","DISTINCT as a crutch instead of diagnosing root cause of duplicates","Running expensive CTEs multiple times — use temp tables in this case"],
    "tips":["The cheapest optimization: select only columns you need","Read EXPLAIN output: Seq Scan on large tables = index missing","Ask to create indexes on high-cardinality filter columns (user_id, order_date, status)"],
    "video":"https://www.youtube.com/results?search_query=SQL+query+optimization+performance+tuning+tutorial"
  },
  { "name":"Recursive CTEs — hierarchies and date sequences",
    "desc":"CTEs that reference themselves — for org charts, date series, and graph traversal.",
    "level":"adv","must":False,
    "time":"3 hrs","order":5,
    "why":"Recursive CTEs are needed for two important real-world use cases: organizational hierarchies (manager chains) and generating date/number sequences without a calendar table.",
    "concepts":["Syntax: WITH RECURSIVE cte AS (base_case UNION ALL recursive_part)","Base case: starting rows (seed)","Recursive part: references the CTE itself","Termination: WHERE condition that eventually becomes false","Uses: org hierarchy traversal, date generation, path finding","Depth limit: most DBs have a max recursion depth (often 100)"],
    "keycode":["-- Generate 30 consecutive dates\nWITH RECURSIVE date_series AS (\n  SELECT '2024-01-01'::date AS d\n  UNION ALL\n  SELECT d + 1 FROM date_series\n  WHERE d < '2024-01-30'\n)\nSELECT d FROM date_series;","-- Org hierarchy: find all reports under a manager\nWITH RECURSIVE org AS (\n  SELECT id, name, manager_id, 0 AS depth\n  FROM employees WHERE id = 100 -- start at manager\n  UNION ALL\n  SELECT e.id, e.name, e.manager_id, o.depth + 1\n  FROM employees e JOIN org o ON e.manager_id = o.id\n)\nSELECT * FROM org ORDER BY depth, name;"],
    "realworld":["Generate a full date spine to fill revenue gaps in time-series analysis","Display full org chart with all levels under any manager","Calculate path length in a network or supply chain graph"],
    "interview":["What is a recursive CTE and when would you use it?","How do you generate a sequence of dates without a calendar table?","What prevents infinite recursion in a recursive CTE?"],
    "tasks":["Generate all dates in 2024 using a recursive CTE","Find all employees who report (directly or indirectly) to a specific VP","Generate Fibonacci sequence up to 1000 using recursive CTE"],
    "mistakes":["Missing the stop condition — infinite loop / max recursion error","Base case not selecting from the right starting rows","Joining on wrong column in recursive part — creates wrong hierarchy"],
    "tips":["Test with depth limit: WHERE depth < 10 during development","Use GENERATE_SERIES in PostgreSQL instead of recursive CTE for date series — simpler","Add depth column to track hierarchy level — useful for org chart display"],
    "video":"https://www.youtube.com/results?search_query=SQL+recursive+CTE+tutorial+hierarchy+date+series"
  },
]

PY_BASICS = [
  { "name":"Python setup: Anaconda, virtual environments, Jupyter",
    "desc":"Set up a professional Python data science environment before writing a single line.",
    "level":"beg","must":False,
    "time":"1-2 hrs","order":1,
    "why":"Broken environments waste hours. Setting up properly with conda environments means each project has isolated dependencies and you'll never hit 'it works on my machine' issues.",
    "concepts":["Anaconda distribution: includes Python + 1500 data science packages","conda create -n myenv python=3.11 — create isolated environment","conda activate myenv — switch environment","pip install package — install within active environment","Jupyter Notebook vs JupyterLab vs VS Code — choose one","requirements.txt: pip freeze > requirements.txt for reproducibility"],
    "keycode":["# Terminal commands\nconda create -n analyst python=3.11\nconda activate analyst\npip install pandas numpy matplotlib seaborn plotly scipy scikit-learn","# In Jupyter: check environment\nimport sys\nprint(sys.executable)\nprint(sys.version)","# requirements.txt\npip freeze > requirements.txt\npip install -r requirements.txt"],
    "realworld":["Set up separate environments for different client projects","Share your analysis environment with a colleague via requirements.txt","Upgrade pandas without breaking your other project"],
    "interview":["What is a virtual environment and why should you use one?","What is the difference between conda and pip?","How do you share your Python environment with a teammate?"],
    "tasks":["Create a new conda environment called 'analyst' with Python 3.11","Install the full data science stack: pandas, numpy, matplotlib, seaborn, plotly, scipy","Launch Jupyter Notebook and create your first notebook"],
    "mistakes":["Installing everything in the base environment — conflicts between projects","Mixing conda and pip installs carelessly — can corrupt environment","Forgetting to activate the environment before installing packages"],
    "tips":["Use conda for environment management, pip for package installation within env","JupyterLab is the modern interface — use it over classic Jupyter Notebook","Name environments by project, not by tool: 'fraud_project' not 'pandas_env'"],
    "video":"https://www.youtube.com/results?search_query=anaconda+virtual+environment+setup+Python+data+science"
  },
  { "name":"Variables, data types, operators",
    "desc":"Python's basic building blocks — how data is stored and manipulated.",
    "level":"beg","must":True,
    "time":"2 hrs","order":2,
    "why":"Every Python program starts here. Understanding data types prevents silent bugs like string concatenation instead of numeric addition.",
    "concepts":["Dynamic typing: Python infers types automatically","int, float, str, bool, NoneType — the 5 fundamental types","type(x) to check type; isinstance(x, int) for type checking","Arithmetic: +, -, *, /, // (floor div), % (modulo), ** (power)","String: immutable, indexable, f-strings for formatting","Boolean: True/False, truthy/falsy values","None: absence of value — not 0, not False, not ''"],
    "keycode":["# F-strings — the modern way\nname = 'Rahul'\nrevenue = 1_250_000.75\nprint(f'Analyst: {name}, Revenue: ₹{revenue:,.0f}')\n\n# Type checking\nprint(type(revenue))  # <class 'float'>\nprint(isinstance(revenue, (int, float)))  # True","# Arithmetic\nprint(10 / 3)   # 3.333... (true division)\nprint(10 // 3)  # 3         (floor division)\nprint(10 % 3)   # 1         (remainder)\nprint(2 ** 10)  # 1024      (power)"],
    "realworld":["Store analyst name and run date in report header variables","Calculate revenue growth rate: (new - old) / old * 100","Track a flag: is_manager = True; format it in SQL query string"],
    "interview":["What is the difference between / and // in Python?","What values are considered 'falsy' in Python?","What is the difference between None and False?"],
    "tasks":["Create variables for name, age, salary and print a formatted summary","Calculate: given monthly salary, compute annual, weekly, and daily amounts","Write code that prints different messages based on whether a value is None vs 0"],
    "mistakes":["0.1 + 0.2 != 0.3 in floating point — use round() or Decimal for money","Comparing None with == instead of 'is None'","Mutable default arguments in functions (a classic Python gotcha)"],
    "tips":["Use f-strings for all string formatting — they're fastest and most readable","Use underscores for large numbers: 1_000_000 is valid and readable","None check: use 'if x is None' not 'if x == None'"],
    "video":"https://www.youtube.com/results?search_query=Python+variables+data+types+tutorial+beginners"
  },
  { "name":"Lists, dicts, tuples, sets — Python data structures",
    "desc":"The four core Python data structures — used constantly in data work.",
    "level":"beg","must":True,
    "time":"3 hrs","order":3,
    "why":"Lists and dicts map directly to real data: a list of rows, a dict of column→value pairs. JSON API responses are dicts. DataFrames are built on these structures.",
    "concepts":["List []: ordered, mutable, allows duplicates. Indexing: list[0], list[-1]","Dict {}: key-value pairs, ordered (Python 3.7+), O(1) lookup","Tuple (): immutable list — use for fixed data, function returns","Set {}: unordered, unique values, O(1) membership check","List slicing: list[start:end:step]","Dict methods: .keys(), .values(), .items(), .get(key, default)","Comprehensions: [x for x in list if condition]"],
    "keycode":["# List operations\ncities = ['Mumbai', 'Delhi', 'Bangalore']\ncities.append('Chennai')\ncities.sort()\nprint(cities[0], cities[-1])  # first, last","# Dict operations\nanalyst = {'name': 'Priya', 'level': 'Senior', 'score': 95}\nprint(analyst.get('salary', 'Not set'))  # safe access\nfor key, val in analyst.items():\n    print(f'{key}: {val}')","# Set for unique values\ncategories = set(['A', 'B', 'A', 'C', 'B'])\nprint(categories)  # {'A', 'B', 'C'}"],
    "realworld":["Store column names as a list, iterate over them","Parse JSON API response (nested dicts) to extract values","Use set to find unique user IDs before counting"],
    "interview":["What is the difference between a list and a tuple? When would you use each?","How do you safely access a dict key that might not exist?","How do you find the intersection of two lists in Python?"],
    "tasks":["Create a list of 5 product names, sort them, add two more, remove one","Build a dict representing an order — add discount key, update price, delete cost","Convert a list with duplicates to unique values using set, then sort it"],
    "mistakes":["list.sort() modifies in place; sorted(list) returns new list","Dict.get() vs dict[key] — the former is safe, the latter throws KeyError","Modifying a list while iterating over it — use a copy instead"],
    "tips":["list comprehension is faster and more Pythonic than a for loop that appends","dict.get(key, default) is your best friend — avoids KeyError","Prefer tuples for data that shouldn't change: coordinates, RGB colors"],
    "video":"https://www.youtube.com/results?search_query=Python+lists+dictionaries+tuples+sets+tutorial"
  },
  { "name":"Functions: def, return, *args, **kwargs, lambda",
    "desc":"Package reusable logic into functions — the foundation of maintainable data code.",
    "level":"beg","must":True,
    "time":"2.5 hrs","order":4,
    "why":"Every data pipeline is a series of functions. Without functions, you copy-paste code endlessly — when the logic changes, you miss an update. Functions are how professionals build data tools.",
    "concepts":["def function_name(params): return value","Default parameters: def f(x, n=10) — n has default value","*args: variable positional arguments (tuple inside function)","**kwargs: variable keyword arguments (dict inside function)","Lambda: anonymous single-expression function","Docstrings: triple-quote documentation inside function","Return multiple values: return a, b (automatically a tuple)"],
    "keycode":["def calculate_growth(current, previous, decimals=2):\n    \"\"\"Calculate period-over-period growth rate.\"\"\"\n    if previous == 0:\n        return None\n    return round((current - previous) / previous * 100, decimals)\n\nprint(calculate_growth(120, 100))  # 20.0\nprint(calculate_growth(120, 100, decimals=0))  # 20","# Lambda in pandas\ndf['tier'] = df['spend'].apply(lambda x: 'VIP' if x > 10000 else 'Standard')\n\n# *args and **kwargs\ndef summarize(*metrics, **settings):\n    for m in metrics:\n        print(f'{m}: calculated')\n    print(settings)"],
    "realworld":["Reusable clean_dataframe() function for every new project","A calculate_cac() function that takes spend and users as parameters","A format_currency() lambda used in pandas apply()"],
    "interview":["What is the difference between *args and **kwargs?","Why are mutable default arguments dangerous in Python?","How do you return multiple values from a function?"],
    "tasks":["Write a clean_column_names(df) function that lowercases and replaces spaces with underscores","Write a calculate_retention(cohort, period_users) function","Use lambda to create a tier label function and apply it to a pandas column"],
    "mistakes":["Mutable default argument: def f(lst=[]) — the list persists between calls! Use None instead","Returning None accidentally — always check that all code paths return something","Long lambda expressions — if it needs more than one operation, use def"],
    "tips":["Write docstrings for all functions: what does it do, what are the params, what does it return","Use type hints for clarity: def f(df: pd.DataFrame, col: str) -> pd.Series","Test every function with edge cases: empty input, None, zero divisor"],
    "video":"https://www.youtube.com/results?search_query=Python+functions+def+lambda+args+kwargs+tutorial"
  },
  { "name":"List comprehensions, loops, and conditionals",
    "desc":"Pythonic iteration and filtering — faster and more readable than traditional loops.",
    "level":"beg","must":True,
    "time":"2 hrs","order":5,
    "why":"List comprehensions replace verbose for loops with clean one-liners. They're 30-50% faster than equivalent loops and are the expected style in professional Python code.",
    "concepts":["[expr for item in iterable if condition] — list comprehension","Dict comprehension: {k:v for k,v in items.items() if condition}","Generator expression: (x for x in iterable) — lazy, memory efficient","for x in list, for i, x in enumerate(list), for a, b in zip(l1, l2)","if/elif/else: indentation-based blocks","Ternary: value_if_true if condition else value_if_false","break, continue, pass in loops"],
    "keycode":["# List comprehension vs loop\nsquares = [x**2 for x in range(10) if x % 2 == 0]\n# Equivalent but slower:\nsquares = []\nfor x in range(10):\n    if x % 2 == 0:\n        squares.append(x**2)","# Dict comprehension from two lists\ncols = ['name', 'age', 'salary']\nvals = ['Priya', 29, 85000]\nrecord = {k: v for k, v in zip(cols, vals)}\nprint(record)","# Ternary expression\nstatus = 'Senior' if salary > 100000 else 'Junior'"],
    "realworld":["Clean a list of column names in one line","Build a lookup dict from two parallel lists (keys and values)","Filter a list of file paths to only CSVs"],
    "interview":["What is a list comprehension and how does it differ from a regular for loop?","When would you use a generator expression instead of a list comprehension?","How do you iterate over a dict's key-value pairs?"],
    "tasks":["Use list comprehension to standardize column names: lowercase, strip spaces, replace spaces with _","Build a dict mapping product_id to product_name from two lists","Filter a list of order amounts to only those > 500 using comprehension"],
    "mistakes":["Overly complex comprehensions — if it needs 3 conditions and nesting, use a for loop","Iterating over a list while modifying it — use a copy","Using list comprehension to create a list you immediately discard — use a generator"],
    "tips":["Any for loop that builds a new list can become a list comprehension","Use enumerate() whenever you need both index and value in a loop","Generator expressions are memory-efficient for large sequences you only iterate once"],
    "video":"https://www.youtube.com/results?search_query=Python+list+comprehension+loops+tutorial"
  },
  { "name":"Error handling: try/except, file I/O, modules",
    "desc":"Write code that handles unexpected inputs gracefully without crashing.",
    "level":"beg","must":False,
    "time":"2 hrs","order":6,
    "why":"Data pipelines encounter bad data, missing files, and API failures constantly. Robust error handling is what separates production-grade code from Jupyter notebook hacks.",
    "concepts":["try/except/finally: catch specific errors","except ValueError as e: handle specific exception type","finally: always executes (file close, cleanup)","raise: throw your own exception","with open('file') as f: context manager auto-closes","os.path.exists() before reading files","logging module for production debugging"],
    "keycode":["import logging\nlogging.basicConfig(level=logging.INFO)\n\ndef load_data(filepath):\n    try:\n        df = pd.read_csv(filepath)\n        logging.info(f'Loaded {len(df)} rows from {filepath}')\n        return df\n    except FileNotFoundError:\n        logging.error(f'File not found: {filepath}')\n        return None\n    except pd.errors.EmptyDataError:\n        logging.warning(f'File is empty: {filepath}')\n        return pd.DataFrame()","# Safe file write\nwith open('output.csv', 'w') as f:\n    df.to_csv(f, index=False)"],
    "realworld":["Handle missing files in a monthly report automation script","Catch API errors and retry with exponential backoff","Log every data transformation step for audit trail"],
    "interview":["What is the difference between except Exception and except ValueError?","Why should you use 'with open()' instead of open() + close()?","How do you log errors in a production Python script?"],
    "tasks":["Write a safe CSV loader that returns None and logs if the file doesn't exist","Add try/except to a function that divides revenue by units — handle ZeroDivisionError","Set up basic logging that writes INFO and above to a log file"],
    "mistakes":["Catching all exceptions with bare except — hides bugs you should fix","Not using with open() — file stays open if exception occurs before .close()","Using print() for debugging in production — use logging instead"],
    "tips":["Always catch specific exceptions, not bare except — be explicit","logging.basicConfig(level=logging.INFO, filename='app.log') for file logging","Use pathlib.Path for file paths — cleaner than os.path"],
    "video":"https://www.youtube.com/results?search_query=Python+error+handling+try+except+tutorial"
  },
]

PY_PANDAS = [
  { "name":"Reading data: read_csv, read_excel, read_sql with best practices",
    "desc":"Load data correctly with proper dtypes, date parsing, and null handling from the start.",
    "level":"beg","must":True,
    "time":"2 hrs","order":1,
    "why":"How you read data determines the quality of everything downstream. Wrong dtypes, unparsed dates, and unhandled nulls cause silent bugs throughout the analysis.",
    "concepts":["pd.read_csv(path, dtype={}, parse_dates=[], na_values=[], encoding='utf-8')","Always specify dtype for ID columns as str (prevents '007' → 7)","parse_dates converts date columns automatically","na_values=['N/A','-','null',''] handles non-standard missing markers","chunksize for large files that don't fit in RAM","pd.read_sql(query, connection) for database queries","pd.read_excel(path, sheet_name=0) for Excel files"],
    "keycode":["import pandas as pd\n\ndf = pd.read_csv('orders.csv',\n    dtype={'order_id': str, 'user_id': str},\n    parse_dates=['order_date', 'ship_date'],\n    na_values=['N/A', 'null', '-', ''],\n    encoding='utf-8'\n)\n\n# Quick validation after load\nprint(df.shape)\nprint(df.dtypes)\nprint(df.isnull().sum())","# Read SQL\nfrom sqlalchemy import create_engine\nengine = create_engine('postgresql://user:pass@host/db')\ndf = pd.read_sql('SELECT * FROM orders WHERE date >= \\'2024-01-01\\'', engine)"],
    "realworld":["Load a CRM export where customer IDs have leading zeros (must be str)","Read a finance file where '-' means zero and 'N/A' means missing","Connect Python directly to PostgreSQL for automated reporting"],
    "interview":["Why should you specify dtype={'id': str} when reading CSVs?","How do you read a CSV file that is too large to fit in memory?","How do you handle non-standard missing value markers like '-' or 'N/A'?"],
    "tasks":["Read orders.csv with proper dtypes — verify order_id is str, date is datetime","Add na_values for your organization's missing data markers","Read data directly from a SQL query using read_sql and SQLAlchemy"],
    "mistakes":["Not specifying dtypes — pandas guesses, often wrong for IDs and dates","Using read_csv without encoding='utf-8' — breaks on special characters (Indian names!)","Loading a 2GB file with default settings — use chunksize instead"],
    "tips":["Always do df.dtypes immediately after read_csv — verify types are correct","parse_dates=['col'] is faster than df['col'] = pd.to_datetime(df['col']) after loading","engine.dispose() after SQL reads to close the connection pool properly"],
    "video":"https://www.youtube.com/results?search_query=pandas+read_csv+read_sql+tutorial+python+data+analysis"
  },
  { "name":"DataFrame exploration: shape, dtypes, describe, isnull, nunique",
    "desc":"The 5-command sequence every analyst runs on any new dataset in the first 60 seconds.",
    "level":"beg","must":True,
    "time":"1.5 hrs","order":2,
    "why":"You cannot analyze data you don't understand. These 5 commands tell you the shape, types, completeness, uniqueness, and distribution of your data before writing a single analytical line.",
    "concepts":["df.shape: (rows, columns) tuple","df.dtypes: column names and their types","df.isnull().sum(): count of nulls per column","df.nunique(): count of unique values per column","df.describe(include='all'): stats for numeric and categorical","df.info(): compact summary of dtypes + non-null counts","df.head(n), df.tail(n), df.sample(n): see actual data"],
    "keycode":["# The 5-command EDA opener\nprint('Shape:', df.shape)\nprint('\\nDtypes:')\nprint(df.dtypes)\nprint('\\nMissing (%):')\nprint(df.isnull().mean().mul(100).round(1).to_string())\nprint('\\nUnique counts:')\nprint(df.nunique().to_string())\ndf.describe(include='all').round(2)","# Value distribution of categorical column\ndf['status'].value_counts(normalize=True).mul(100).round(1)"],
    "realworld":["First look at a new dataset from a client before cleaning","Check data quality: are there any columns with >20% missing?","Understand cardinality: is 'city' a real city name or a code with 3 values?"],
    "interview":["What is the first thing you do when you receive a new dataset?","How do you check for missing values in a DataFrame?","What does describe() show for non-numeric columns?"],
    "tasks":["Run the 5-command EDA sequence on the Titanic or any Kaggle dataset","Find all columns with >10% missing values","Check if 'user_id' is truly unique (nunique should equal len(df))"],
    "mistakes":["Jumping into analysis without checking dtypes — dates as objects, IDs as int","Ignoring missing values until they cause wrong analysis","Trusting describe() without checking if categorical columns are correctly typed"],
    "tips":["df.isnull().mean().mul(100).round(1) gives % missing — more useful than count","df.info() shows memory usage — useful for large DataFrames","df['col'].value_counts().head(10) shows the most common values — always run for categoricals"],
    "video":"https://www.youtube.com/results?search_query=pandas+DataFrame+exploration+EDA+tutorial+Python"
  },
  { "name":"loc, iloc, boolean filtering — selecting subsets",
    "desc":"Select specific rows and columns precisely — the most-used daily pandas skill.",
    "level":"beg","must":True,
    "time":"2 hrs","order":3,
    "why":"Every data manipulation starts with selecting the right subset. loc/iloc are used hundreds of times per analysis. Confusing them causes subtle bugs.",
    "concepts":["df['col']: Series. df[['col1','col2']]: DataFrame (note double brackets)","df.loc[row_label, col_name]: label-based — uses actual index values","df.iloc[row_int, col_int]: position-based — 0-indexed integer positions","Boolean mask: df[df['age'] > 30] or df.loc[df['age'] > 30]","Multiple conditions: df[(cond1) & (cond2)] — must use () around each","df.loc[mask, ['col1','col2']]: filter rows AND select specific columns","isin(): df[df['city'].isin(['Mumbai','Delhi'])]"],
    "keycode":["# Selecting columns\ndf['revenue']              # Series\ndf[['name', 'revenue']]    # DataFrame\n\n# loc: label-based\ndf.loc[df['status'] == 'active', ['name', 'revenue']]\n\n# iloc: position-based\ndf.iloc[0:5, 0:3]  # first 5 rows, first 3 columns\n\n# Multiple conditions\ndf[(df['revenue'] > 1000) & (df['region'].isin(['North','South']))]\n\n# .copy() to avoid SettingWithCopyWarning\nhigh_value = df.loc[df['revenue'] > 5000].copy()"],
    "realworld":["Filter to only active customers and select 3 key columns for a report","Get top 10 rows by revenue using iloc after sorting","Filter to last 30 days AND region='North' for a regional report"],
    "interview":["What is the difference between .loc and .iloc?","Why do you need double brackets df[['col']] to get a DataFrame instead of Series?","How do you filter rows where a date column is in the last 7 days?"],
    "tasks":["Select rows where salary > 80000 AND department is in ['Engineering','Product']","Use iloc to get the last 5 rows and first 3 columns","Use .loc to update the status column to 'VIP' for customers with spend > 10000"],
    "mistakes":["df['col1','col2'] (wrong) vs df[['col1','col2']] (correct)","Using .iloc on a sorted/filtered DataFrame — positions shift after sort","Not using .copy() after filtering — SettingWithCopyWarning on assignment"],
    "tips":["Always use .copy() when creating a filtered subset you'll modify","df.query('revenue > 1000 and region == \"North\"') is a readable alternative to boolean masks","df.loc[mask, col] = value is the correct way to set values on a filtered subset"],
    "video":"https://www.youtube.com/results?search_query=pandas+loc+iloc+boolean+filtering+tutorial"
  },
  { "name":"groupby() — agg, transform, apply, named aggregations",
    "desc":"The pandas equivalent of SQL GROUP BY — the most important data aggregation tool.",
    "level":"int","must":True,
    "time":"3 hrs","order":4,
    "why":"groupby is the backbone of analytics. Revenue by region, users by channel, orders by month — all use groupby. The agg/transform/apply distinction is tested in every Python data interview.",
    "concepts":["df.groupby('col')['metric'].agg(['mean','sum','count'])","Named aggregations: .agg(avg_rev=('revenue','mean'), total=('revenue','sum'))","transform(): returns same-length Series (unlike agg which collapses)","apply(): apply custom function to each group — flexible but slower","GroupBy on multiple columns: df.groupby(['region','product'])","as_index=False: return flat DataFrame instead of grouped index","reset_index() after groupby to flatten MultiIndex"],
    "keycode":["# Named aggregations — clean column names\nresult = df.groupby('region').agg(\n    total_revenue=('amount', 'sum'),\n    order_count=('order_id', 'nunique'),\n    avg_order=('amount', 'mean'),\n    customer_count=('user_id', 'nunique')\n).round(2)\n\n# transform: add group-level stat to every row\ndf['region_avg'] = df.groupby('region')['revenue'].transform('mean')\ndf['above_avg'] = df['revenue'] > df['region_avg']","# apply with custom function\ndef top_3(group):\n    return group.nlargest(3, 'revenue')\ndf.groupby('region').apply(top_3)"],
    "realworld":["Monthly revenue breakdown by region and product for a dashboard","Add department average salary to each employee row using transform","Find top 3 customers per region using apply(nlargest)"],
    "interview":["What is the difference between groupby agg() and transform()?","How do you perform multiple aggregations and give them clean column names?","How do you calculate a group-level average and add it to the original DataFrame?"],
    "tasks":["Build a regional sales summary: sum revenue, count unique orders and customers","Use transform to add a 'dept_avg_salary' column — calculate if each employee is above/below average","Use apply to get the top 3 orders per product category"],
    "mistakes":["Forgetting reset_index() — leaving a confusing GroupBy MultiIndex","Using apply() for simple aggregations — agg() is much faster","Not using nunique for counting unique users — count() counts non-null rows"],
    "tips":["Named agg syntax: .agg(new_name=('original_col', 'func')) — use always","transform is the pandas equivalent of SQL window function without collapsing rows","groupby(['col1','col2']) creates MultiIndex — reset_index() to flatten"],
    "video":"https://www.youtube.com/results?search_query=pandas+groupby+agg+transform+tutorial+Python"
  },
  { "name":"merge() and concat() — joining DataFrames",
    "desc":"Combine DataFrames by key columns (merge) or by stacking (concat) — pandas' JOIN operations.",
    "level":"int","must":True,
    "time":"2.5 hrs","order":5,
    "why":"Real data lives in multiple tables. Every analysis joins user attributes to orders, products to categories, campaigns to revenue. Merge is the most-used data operation after groupby.",
    "concepts":["pd.merge(left, right, on='key', how='left') — SQL JOIN equivalent","how: 'inner','left','right','outer'","left_on/right_on for different column names: merge(a, b, left_on='user_id', right_on='id')","validate parameter: '1:1','1:m','m:1','m:m' — catches unexpected duplicates","pd.concat([df1, df2], ignore_index=True) — stack vertically","suffixes=('_x','_y') for overlapping column names","indicator=True adds _merge column showing match status"],
    "keycode":["# Standard left join with validation\nresult = pd.merge(\n    orders, users,\n    left_on='user_id', right_on='id',\n    how='left',\n    validate='m:1',  # many orders, one user\n    suffixes=('_order', '_user')\n)\nprint(f'Rows before: {len(orders)}, after: {len(result)}')\n\n# Stack monthly files\nall_months = pd.concat([jan, feb, mar, apr], ignore_index=True)\nprint(all_months.shape)","# Find unmatched rows\nresult = pd.merge(a, b, on='id', how='left', indicator=True)\nunmatched = result[result['_merge'] == 'left_only']"],
    "realworld":["Add customer name, city, and segment to every order","Stack 12 monthly CSV files into one DataFrame for annual analysis","Find orders with no matching user record (data quality check)"],
    "interview":["How do you merge two DataFrames with different column names for the key?","What does the validate parameter in merge() do?","When would you use concat instead of merge?"],
    "tasks":["Merge orders with users (left join) — check row count before and after","Use indicator=True to find orders with no matching product","Stack 3 monthly DataFrames and reset the index"],
    "mistakes":["Merge without checking validate — many-to-many silently multiplies rows","Not checking row count after merge — unexpected inflation goes unnoticed","Using concat to join on keys — that's what merge is for"],
    "tips":["Always print len() before and after merge — verify expected row count","validate='m:1' catches the most common accidental many-to-many join","Use pd.merge() explicitly, not df.merge() — clearer which is left/right"],
    "video":"https://www.youtube.com/results?search_query=pandas+merge+concat+join+tutorial+Python"
  },
  { "name":"pivot_table, melt, crosstab — reshaping DataFrames",
    "desc":"Transform data between wide and long formats — essential for reporting and visualization.",
    "level":"int","must":True,
    "time":"2.5 hrs","order":6,
    "why":"Data rarely comes in the shape you need for a report. pivot_table builds cross-tab matrices (monthly revenue by product). melt converts wide Excel exports to analysis-ready long format.",
    "concepts":["pivot_table: rows=index, cols=columns, values=values, aggfunc='sum'","fill_value=0 for NaN in pivot output","margins=True adds row/column totals","melt: wide → long, id_vars stay, value_vars become rows","pd.crosstab: frequency cross-tabulation between two categorical columns","crosstab(normalize='index') for row-wise percentages","stack()/unstack() for MultiIndex reshaping"],
    "keycode":["# Pivot table: monthly revenue by region\npivot = df.pivot_table(\n    values='revenue',\n    index='region',\n    columns='month',\n    aggfunc='sum',\n    fill_value=0,\n    margins=True\n)\n\n# Melt: wide monthly columns → long format\ndf_long = df.melt(\n    id_vars=['product_id', 'product_name'],\n    value_vars=['jan', 'feb', 'mar', 'apr'],\n    var_name='month',\n    value_name='revenue'\n)\n\n# Crosstab with percentages\npd.crosstab(df['gender'], df['purchased'],\n           normalize='index').mul(100).round(1)"],
    "realworld":["Build a region × month revenue matrix for a board presentation","Convert wide Excel export (months as columns) to long format for seaborn plotting","Show purchase rate by gender and age group with crosstab"],
    "interview":["What is the difference between pivot_table and melt?","When would you use melt? Give a real example.","How do you add row and column totals to a pivot table?"],
    "tasks":["Build a product × month revenue pivot table with fill_value=0 and margins=True","Melt a quarterly revenue DataFrame from wide to long format for visualization","Create a crosstab showing % of customers by segment who made a repeat purchase"],
    "mistakes":["Forgetting fill_value=0 — NaN in pivot creates confusing output","Forgetting reset_index() after pivot_table — pivot index becomes confusing","Using pivot() instead of pivot_table() when there are duplicates — raises error"],
    "tips":["margins=True adds 'All' row and column — great for sanity checking totals","pivot_table is essentially a pandas GROUP BY with reshaping","After melt, sort_values(['id','month']) to restore logical order"],
    "video":"https://www.youtube.com/results?search_query=pandas+pivot_table+melt+reshape+tutorial+Python"
  },
  { "name":"Time-series operations: rolling, cumsum, shift, diff, .dt accessor",
    "desc":"Work with dates and time-based calculations — essential for trends, moving averages, and period comparisons.",
    "level":"int","must":True,
    "time":"2.5 hrs","order":7,
    "why":"Most business metrics are time-based: 7-day moving average, month-over-month change, cumulative revenue. These operations are used daily in any analyst role.",
    "concepts":["df['col'].rolling(7).mean() — 7-period moving average","rolling(min_periods=1) — calculate even for first N-1 rows","cumsum() — running total","shift(1) — previous row value (LAG equivalent)","diff(1) — current minus previous (WoW/MoM change)","pct_change(1) — % change from previous row",".dt accessor: .dt.year, .dt.month, .dt.dayofweek, .dt.hour, .dt.quarter","groupby().transform(lambda x: x.rolling(7).mean()) — rolling per group"],
    "keycode":["# Ensure sorted by date first!\ndf = df.sort_values('date')\n\n# 7-day moving average\ndf['ma_7d'] = df['revenue'].rolling(7, min_periods=1).mean().round(2)\n\n# Month-over-month change\ndf['prev_month'] = df.groupby('product')['revenue'].shift(1)\ndf['mom_change'] = df['revenue'] - df['prev_month']\ndf['mom_pct'] = df['revenue'].pct_change(1).mul(100).round(1)\n\n# Running total\ndf['cumulative_rev'] = df.groupby('region')['revenue'].cumsum()\n\n# Extract date parts\ndf['year'] = df['date'].dt.year\ndf['month'] = df['date'].dt.month\ndf['dow'] = df['date'].dt.day_name()"],
    "realworld":["Weekly active users trend with 4-week rolling average","Month-over-month revenue change per product for a dashboard","Cumulative revenue for a fiscal year starting April 1"],
    "interview":["How do you calculate a 7-day rolling average in pandas?","How do you calculate month-over-month change using pandas?","How do you extract the day of week from a datetime column?"],
    "tasks":["Calculate 7-day and 30-day moving average on daily sales data","Add a pct_change column showing WoW % change in orders","Create date feature columns: year, month, quarter, day_of_week, is_weekend"],
    "mistakes":["Forgetting to sort by date before rolling/cumsum — wrong results silently","Not using groupby before shift() — shift crosses group boundaries","Rolling without min_periods=1 — NaN for the first N-1 rows"],
    "tips":["Always sort_values('date') before any time-series operation","df['is_weekend'] = df['date'].dt.dayofweek >= 5 — clean boolean flag","period = df['date'].dt.to_period('M') for clean month labels in groupby"],
    "video":"https://www.youtube.com/results?search_query=pandas+rolling+cumsum+shift+time+series+tutorial"
  },
  { "name":"Handling missing values: isnull, fillna, dropna, imputation strategies",
    "desc":"Detect, understand, and thoughtfully handle missing data — one of the most important data cleaning skills.",
    "level":"int","must":True,
    "time":"2 hrs","order":8,
    "why":"Real-world data is always messy with missing values. How you handle them affects the validity of your entire analysis. Different missingness mechanisms require different strategies.",
    "concepts":["MCAR: Missing Completely At Random — safe to drop if <5%","MAR: Missing At Random — impute with mean/median/mode","MNAR: Missing Not At Random — domain knowledge needed","df.isnull().mean() * 100 — % missing per column","fillna(value): replace with constant","fillna(method='ffill') or ffill(): forward fill (time series)","dropna(subset=['key_col']): drop only if specific column is null","interpolate(): linear interpolation for time series"],
    "keycode":["# Assess missingness\nprint(df.isnull().mean().mul(100).round(1).sort_values(ascending=False))\n\n# Different strategies by column type\ndf_clean = df.copy()\n# Numeric: fill with median\ndf_clean['revenue'].fillna(df_clean['revenue'].median(), inplace=True)\n# Categorical: fill with mode\ndf_clean['category'].fillna(df_clean['category'].mode()[0], inplace=True)\n# Time-series: forward fill\ndf_clean['daily_price'] = df_clean['daily_price'].ffill()\n# Drop rows where key column is null\ndf_clean = df_clean.dropna(subset=['user_id', 'order_date'])","# Add missingness flag (important for analysis)\ndf['revenue_was_null'] = df['revenue'].isnull().astype(int)"],
    "realworld":["CRM export with 15% missing phone numbers — strategy: flag, don't drop","Financial data with gaps on holidays — forward fill price data","Survey data with optional questions — leave NULL, filter in analysis"],
    "interview":["How do you handle missing values? What factors affect your strategy?","What is the difference between dropna() and fillna()?","When would you use forward fill vs median imputation?"],
    "tasks":["Assess missingness in a dataset and categorize columns by % missing","Apply appropriate strategy: median for revenue, mode for category, ffill for dates","Add is_imputed flag columns for any column you impute"],
    "mistakes":["Dropping rows with any null — can lose 90% of data if many columns have even 1% missing","Filling numerics with 0 when 0 has a different meaning than 'unknown'","Not documenting imputation decisions — analysis becomes unreproducible"],
    "tips":["Rule of thumb: <5% missing = consider drop; 5-30% = impute; >30% = consider dropping column","Always add _was_null flag before imputing — preserves the information that data was missing","df.dropna(subset=['user_id']) is safer than df.dropna() — only drops on critical columns"],
    "video":"https://www.youtube.com/results?search_query=pandas+missing+values+fillna+dropna+tutorial"
  },
  { "name":"Vectorized operations with NumPy: np.where, np.select, broadcasting",
    "desc":"Use NumPy's C-speed array operations instead of Python loops — 100x+ faster.",
    "level":"int","must":True,
    "time":"2 hrs","order":9,
    "why":"pandas is built on NumPy. Using vectorized operations instead of apply(lambda) or iterrows() is the difference between a query that takes 1 second vs 10 minutes on 1M rows.",
    "concepts":["np.where(condition, val_true, val_false) — CASE WHEN equivalent","np.select(conditions_list, choices_list, default) — multi-branch CASE WHEN","Broadcasting: operations apply to entire array at once","df['col'] * 2 — vectorized (C-speed). for row in df (Python-speed)","Avoid iterrows() — 1000x slower than vectorized","np.where is faster than apply(lambda) by 10-100x"],
    "keycode":["import numpy as np\n\n# np.where — 2-branch conditional (like IF ELSE)\ndf['tier'] = np.where(df['ltv'] > 5000, 'Premium', 'Standard')\n\n# np.select — multi-branch (like CASE WHEN)\nconditions = [\n    df['score'] >= 90,\n    df['score'] >= 70,\n    df['score'] >= 50\n]\nchoices = ['A', 'B', 'C']\ndf['grade'] = np.select(conditions, choices, default='F')\n\n# Vectorized math\ndf['revenue_usd'] = df['revenue_inr'] / 83.5\ndf['is_weekend'] = df['date'].dt.dayofweek >= 5"],
    "realworld":["Classify customers into 4 tiers based on LTV without any loop","Apply currency conversion to entire revenue column in one line","Create a risk flag: high_risk = spend > 2x average AND age < 25"],
    "interview":["Why should you avoid iterrows() in pandas?","What is the difference between np.where and np.select?","What does broadcasting mean in NumPy?"],
    "tasks":["Replace a for loop that creates a tier column with np.where","Use np.select to create a 5-level customer segment from 4 conditions","Benchmark: compare iterrows() vs apply() vs np.where on 100,000 rows with %%timeit"],
    "mistakes":["Using apply(lambda x: ...) for single-column operations that have vectorized equivalents","Not using np.select for 3+ conditions — nested np.where becomes unreadable","Modifying DataFrame inside a loop — assign the whole vectorized result at once"],
    "tips":["%%timeit in Jupyter to benchmark your code — see the difference yourself","np.select is cleaner than nested np.where for 3+ conditions","df.assign(new_col=np.where(...)) is a clean way to add columns without inplace"],
    "video":"https://www.youtube.com/results?search_query=numpy+where+select+vectorized+operations+pandas+tutorial"
  },
]

PY_VIZ = [
  { "name":"Matplotlib fundamentals: Figure, Axes, subplots",
    "desc":"Build charts from the ground up using matplotlib's object-oriented API.",
    "level":"beg","must":True,
    "time":"2.5 hrs","order":1,
    "why":"Matplotlib is the foundation of Python visualization. seaborn, pandas.plot(), and many other libraries use matplotlib under the hood. Understanding the Figure/Axes architecture unlocks full customization.",
    "concepts":["fig, ax = plt.subplots() — create Figure and Axes objects","Figure: the entire canvas. Axes: individual chart area","ax.plot(), ax.bar(), ax.scatter() — draw on specific Axes","plt.subplots(2,3, figsize=(18,10)) — 6 charts in one figure","ax.set_title(), ax.set_xlabel(), ax.set_ylabel() — labels","ax.spines['top'].set_visible(False) — remove chart junk","plt.tight_layout() — prevent overlap between subplots","plt.savefig('chart.png', dpi=150, bbox_inches='tight')"],
    "keycode":["import matplotlib.pyplot as plt\nimport numpy as np\n\nfig, axes = plt.subplots(1, 2, figsize=(14, 5))\n\n# Chart 1: Revenue trend\naxes[0].plot(months, revenue, color='#7c6af7', linewidth=2.5, marker='o')\naxes[0].set_title('Monthly Revenue 2024', fontsize=14, fontweight='bold')\naxes[0].set_xlabel('Month'); axes[0].set_ylabel('Revenue (₹ Lakhs)')\naxes[0].grid(alpha=0.3)\naxes[0].spines['top'].set_visible(False)\naxes[0].spines['right'].set_visible(False)\n\n# Chart 2: Bar chart\naxes[1].bar(categories, values, color='#3b82f6', edgecolor='white')\naxes[1].set_title('Sales by Category', fontsize=14)\n\nplt.tight_layout()\nplt.savefig('dashboard.png', dpi=150, bbox_inches='tight')\nplt.show()"],
    "realworld":["Build a 4-chart analytics dashboard saved as PNG for a stakeholder email","Create a revenue trend chart with annotations for key business events","Side-by-side comparison chart for A/B test results"],
    "interview":["What is the difference between plt.plot() and ax.plot()?","How do you create a figure with multiple charts arranged in a 2×3 grid?","How do you remove the top and right borders from a chart?"],
    "tasks":["Create a 2×2 subplot figure with 4 different chart types on the same dataset","Add value labels on top of each bar using ax.bar_label()","Save a high-resolution PNG (dpi=150) suitable for a presentation"],
    "mistakes":["Using plt.plot() API instead of ax.plot() — inconsistent in multi-chart figures","Not calling tight_layout() — charts overlap each other","Forgetting bbox_inches='tight' in savefig — labels get cut off"],
    "tips":["Always use fig, ax = plt.subplots() — the OO API is clearer for complex charts","plt.style.use('seaborn-v0_8-darkgrid') for instant professional look","Set figsize=(12,6) as default — the default 6.4x4.8 is too small for reports"],
    "video":"https://www.youtube.com/results?search_query=matplotlib+tutorial+python+Figure+Axes+subplots"
  },
  { "name":"Seaborn: heatmaps, boxplots, pairplots for EDA",
    "desc":"Statistical visualizations in one line — seaborn's high-level interface for analyst charts.",
    "level":"int","must":True,
    "time":"2.5 hrs","order":2,
    "why":"Seaborn produces publication-quality statistical charts with far less code than matplotlib. The correlation heatmap, distribution plots, and categorical plots are used in every EDA.",
    "concepts":["sns.heatmap(df.corr(), annot=True, cmap='RdYlGn') — correlation matrix","sns.boxplot, sns.violinplot — distribution comparison across categories","sns.scatterplot with hue= and size= for multivariate visualization","sns.pairplot: scatter matrix for all numeric columns — EDA standard","sns.barplot: mean + CI bar chart","sns.countplot: frequency count by category","sns.set_theme() / sns.set_style() for consistent aesthetics"],
    "keycode":["import seaborn as sns\nimport matplotlib.pyplot as plt\n\n# Correlation heatmap\nfig, ax = plt.subplots(figsize=(12, 8))\nsns.heatmap(df.corr(numeric_only=True), annot=True, fmt='.2f',\n           cmap='RdYlGn', vmin=-1, vmax=1, center=0,\n           square=True, ax=ax)\nax.set_title('Feature Correlation Matrix', fontsize=14)\nplt.tight_layout()\n\n# Distribution comparison\nfig, axes = plt.subplots(1, 2, figsize=(14, 5))\nsns.boxplot(data=df, x='region', y='revenue', ax=axes[0])\nsns.violinplot(data=df, x='region', y='revenue', ax=axes[1])\nplt.tight_layout()"],
    "realworld":["Show feature correlations for a churn analysis EDA","Compare revenue distribution across regions with boxplot","Explore relationships between all numeric variables with pairplot"],
    "interview":["When would you use a boxplot vs a violin plot?","How do you add annotations to a seaborn heatmap?","How do you use hue= in seaborn to add a third dimension to a scatter plot?"],
    "tasks":["Create a correlation heatmap of all numeric columns in a dataset","Build a grouped boxplot: revenue distribution by region colored by product tier","Use pairplot to explore relationships between 5 numeric columns"],
    "mistakes":["Using sns.heatmap on non-numeric columns — pass df.corr(numeric_only=True)","Not setting vmin=-1, vmax=1, center=0 for correlation heatmap — misleading colors","sns.pairplot on too many columns — exponential chart count, becomes unreadable"],
    "tips":["annot=True + fmt='.2f' on heatmap shows rounded correlation values in cells","hue='segment' in any seaborn chart adds automatic color-coded grouping","plt.figure(figsize=...) before sns.pairplot() controls the output size"],
    "video":"https://www.youtube.com/results?search_query=seaborn+heatmap+boxplot+pairplot+tutorial+python"
  },
  { "name":"Plotly Express: interactive charts for dashboards",
    "desc":"Create interactive, web-ready charts with hover tooltips in a single line of code.",
    "level":"int","must":True,
    "time":"2.5 hrs","order":3,
    "why":"Plotly charts are interactive — stakeholders can hover, zoom, filter. They export as self-contained HTML. Every modern analyst dashboard uses Plotly or a library built on it (Dash, Streamlit).",
    "concepts":["import plotly.express as px — the high-level Plotly interface","px.bar, px.line, px.scatter, px.pie, px.box, px.histogram","color=, size=, facet_col=, animation_frame= for rich encoding","fig.update_layout() for titles, font, background, legend","fig.write_html('chart.html') — shareable interactive file","Plotly Graph Objects (go) for full customization","Dash / Streamlit integration for full dashboards"],
    "keycode":["import plotly.express as px\n\n# Interactive bar chart\nfig = px.bar(df_monthly, x='month', y='revenue',\n            color='region', barmode='group',\n            title='Monthly Revenue by Region 2024',\n            text_auto=True)\nfig.update_layout(font_family='Arial', template='plotly_dark')\nfig.write_html('revenue_chart.html')\nfig.show()\n\n# Interactive scatter with trendline\nfig2 = px.scatter(df, x='cac', y='ltv', color='channel',\n                 size='revenue', hover_data=['customer_id'],\n                 trendline='ols',\n                 title='LTV vs CAC by Acquisition Channel')\nfig2.show()"],
    "realworld":["Revenue dashboard with region filter sent to stakeholder as HTML","Interactive scatter showing LTV vs CAC by acquisition channel","Funnel chart for checkout conversion with hover details"],
    "interview":["How is Plotly different from matplotlib for stakeholder presentations?","How do you save a Plotly chart that a non-technical person can view without Python?","What is the difference between Plotly Express and Plotly Graph Objects?"],
    "tasks":["Build an interactive bar chart with color grouping and text labels","Create a scatter plot with hover showing customer_id and revenue details","Export a chart as standalone HTML and verify it works without Python"],
    "mistakes":["fig.show() in a script (not Jupyter) — opens browser; use write_html instead","Using Plotly for static PDF reports — matplotlib is better for that use case","Not setting template='plotly_white' — dark theme can look unprofessional in emails"],
    "tips":["fig.write_html('chart.html', include_plotlyjs='cdn') — smaller file size","px.funnel() for conversion funnels — no manual calculation needed","animation_frame='month' creates an animated time-lapse chart — great for demos"],
    "video":"https://www.youtube.com/results?search_query=plotly+express+interactive+charts+python+tutorial"
  },
  { "name":"Chart design principles: Tufte, color, data-ink ratio",
    "desc":"Principles that make charts actually communicate insight instead of creating confusion.",
    "level":"int","must":True,
    "time":"1.5 hrs","order":4,
    "why":"A technically correct chart with bad design misleads stakeholders or gets ignored. Data visualization principles are what separate analyst-quality charts from chart junk.",
    "concepts":["Tufte's data-ink ratio: every pixel should carry information — remove decorations","Chart junk: 3D effects, heavy gridlines, unnecessary borders, legends that repeat colors","Pre-attentive attributes: color, size, shape — use to highlight key insights","Color rules: max 5-7 categories; use diverging for +/- (RdYlGn); colorblind-safe","Choosing chart type: line=trend, bar=comparison, scatter=correlation, pie=part-of-whole (<5 slices)","Direct labeling: label data points directly instead of relying on legend","Every chart needs: clear title (insight, not just description), labeled axes, data source"],
    "keycode":["# Professional minimal style\nimport matplotlib.pyplot as plt\n\nplt.rcParams.update({\n    'font.family': 'Arial',\n    'axes.spines.top': False,\n    'axes.spines.right': False,\n    'axes.grid': True,\n    'grid.alpha': 0.3,\n    'axes.labelsize': 12,\n    'axes.titlesize': 14,\n    'axes.titleweight': 'bold'\n})\n\nfig, ax = plt.subplots(figsize=(12, 6))\nbars = ax.bar(categories, values, color='#3b82f6', edgecolor='white', linewidth=0.5)\nax.bar_label(bars, fmt='₹%.0fL', padding=4, fontsize=10)  # direct labels!\nax.set_title('Q1 2024: North Region Leads with 40% of Revenue', fontsize=14)\nax.set_xlabel(''); ax.set_ylabel('Revenue (₹ Lakhs)')"],
    "realworld":["Executive dashboard where every chart communicates a decision-relevant insight","A/B test results chart that clearly shows statistical significance","Regional performance heatmap that highlights underperforming areas"],
    "interview":["How do you choose between a bar chart and a line chart?","What is Tufte's data-ink ratio principle?","How do you make your charts accessible to colorblind viewers?"],
    "tasks":["Take a chart with chart junk and apply data-ink ratio principles to clean it","Redesign a pie chart with 8 segments into a better chart type","Create a diverging color bar chart for MoM change: green = positive, red = negative"],
    "mistakes":["3D charts — impossible to read accurately and only look impressive, not informative","Pie charts with more than 5 slices — use horizontal bar chart instead","Misleading y-axis: not starting at 0 for bar charts exaggerates differences"],
    "tips":["The chart title should be the insight: 'North outperforms all regions by 40%' not 'Revenue by Region'","Remove all gridlines you don't need — horizontal light gray only","Use colorbrewer2.org for perceptually uniform, colorblind-safe palettes"],
    "video":"https://www.youtube.com/results?search_query=data+visualization+best+practices+design+principles+tutorial"
  },
]

PY_STATS = [
  { "name":"Descriptive statistics and outlier detection",
    "desc":"Summarize data distributions and identify anomalies using statistical methods.",
    "level":"beg","must":True,
    "time":"2.5 hrs","order":1,
    "why":"Descriptive statistics are the foundation of every EDA. Outlier detection is performed in every data cleaning step. Both appear in every data analyst interview.",
    "concepts":["Mean vs median: mean sensitive to outliers, median robust","Standard deviation: spread of data. Variance = std²","IQR = Q3 - Q1: range of middle 50%","Skewness: positive = right tail (mean > median). Kurtosis: peakedness","Z-score: (x - mean) / std. |z| > 3 = outlier","IQR method: outliers outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR]","clip(): cap outliers at bounds without removing rows"],
    "keycode":["import pandas as pd, numpy as np\n\n# Full descriptive summary\ndf['revenue'].describe().round(2)\n\n# Z-score outlier detection\ndf['z_score'] = (df['revenue'] - df['revenue'].mean()) / df['revenue'].std()\noutliers_z = df[df['z_score'].abs() > 3]\nprint(f'Z-score outliers: {len(outliers_z)}')\n\n# IQR method\nQ1 = df['revenue'].quantile(0.25)\nQ3 = df['revenue'].quantile(0.75)\nIQR = Q3 - Q1\nlower = Q1 - 1.5 * IQR\nupper = Q3 + 1.5 * IQR\noutliers_iqr = df[(df['revenue'] < lower) | (df['revenue'] > upper)]\n\n# Cap outliers (preserve row count)\ndf['revenue_capped'] = df['revenue'].clip(lower=lower, upper=upper)"],
    "realworld":["Salary analysis: is the mean misleading due to executive outliers?","Transaction amounts: flag unusually large orders for fraud review","Order value distribution: understand the shape before building a model"],
    "interview":["When would you use median instead of mean for a business metric?","What is the IQR method for outlier detection?","What is skewness and what does positive skewness tell you about a distribution?"],
    "tasks":["Calculate full descriptive stats for a revenue column — compare mean vs median","Identify outliers using both z-score and IQR methods — compare results","Plot a histogram + boxplot side by side to visualize the distribution and outliers"],
    "mistakes":["Using mean for highly skewed data — median is more representative","Removing outliers without understanding them — they may be the most important data points","Not visualizing the distribution — raw stats alone can be misleading"],
    "tips":["Always compare mean vs median: large difference = skewed distribution or outliers","df.quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]) for full picture","Visualize first: histogram + boxplot before deciding on outlier treatment strategy"],
    "video":"https://www.youtube.com/results?search_query=pandas+descriptive+statistics+outlier+detection+tutorial"
  },
  { "name":"Hypothesis testing: t-test, chi-square, p-values",
    "desc":"Test whether observed differences are statistically significant or just random noise.",
    "level":"int","must":True,
    "time":"3.5 hrs","order":2,
    "why":"Hypothesis testing is the core of A/B testing — the most common advanced analytical task at product companies. Every recommendation about feature changes, pricing, or UX needs statistical validation.",
    "concepts":["H0 (null): no effect. H1 (alternative): there is an effect","p-value: probability of observing this result if H0 were true","Significance level α: typically 0.05. If p < α, reject H0","Type I error (false positive): reject H0 when it's true (α)","Type II error (false negative): fail to reject H0 when it's false (β)","T-test: compare means of numeric variable between 2 groups","Chi-square: test independence between 2 categorical variables","Effect size (Cohen's d): how big is the difference, not just is it significant"],
    "keycode":["from scipy import stats\nimport numpy as np\n\n# Two-sample t-test (A/B test)\ncontrol = df[df['variant'] == 'control']['conversion_rate']\ntreatment = df[df['variant'] == 'treatment']['conversion_rate']\n\nt_stat, p_value = stats.ttest_ind(control, treatment, equal_var=False)\neffect_size = (treatment.mean() - control.mean()) / np.sqrt(\n    (control.std()**2 + treatment.std()**2) / 2\n)\n\nprint(f'Control mean: {control.mean():.4f}')\nprint(f'Treatment mean: {treatment.mean():.4f}')\nprint(f'Lift: {(treatment.mean()/control.mean()-1)*100:.2f}%')\nprint(f'p-value: {p_value:.4f}')\nprint(f'Significant: {\"YES\" if p_value < 0.05 else \"NO\"}')\nprint(f\"Cohen's d: {effect_size:.3f}\")\n\n# Chi-square test\ncrosstab = pd.crosstab(df['gender'], df['purchased'])\nchi2, p, dof, expected = stats.chi2_contingency(crosstab)\nprint(f'Chi-square p-value: {p:.4f}')"],
    "realworld":["A/B test: does the new checkout button increase conversion rate significantly?","Does discount tier affect average order value (t-test across 2 groups)?","Is purchase rate independent of device type? (chi-square)"],
    "interview":["What is a p-value? Explain it to a non-technical stakeholder.","What is the difference between statistical significance and practical significance?","Why do you use equal_var=False in ttest_ind?"],
    "tasks":["Run a t-test comparing revenue between two user segments — interpret results in plain English","Run a chi-square test on device type vs purchase conversion — is device predictive?","Calculate Cohen's d for your A/B test and interpret: small/medium/large effect"],
    "mistakes":["Stopping an A/B test early when results look significant — p-hacking","Reporting p-value without effect size — significance without magnitude is incomplete","Using t-test when data is heavily non-normal and sample size is small — use Mann-Whitney U instead"],
    "tips":["p < 0.05 means 95% confidence, not 95% chance the result is true — subtle distinction","Always report: lift %, p-value, confidence interval, sample size, and effect size","statsmodels.stats.power.TTestIndPower for pre-test sample size calculation"],
    "video":"https://www.youtube.com/results?search_query=hypothesis+testing+t-test+python+scipy+tutorial+A/B+test"
  },
  { "name":"A/B test analysis end-to-end in Python",
    "desc":"Full A/B test workflow: design, analysis, interpretation, and recommendation.",
    "level":"int","must":True,
    "time":"4 hrs","order":3,
    "why":"A/B testing analysis is the #1 advanced skill tested at product companies (Flipkart, Meesho, Swiggy, CRED, Razorpay). It combines statistics, business thinking, and Python coding.",
    "concepts":["Step 1: Define primary metric and guardrail metrics","Step 2: Pre-test sample size calculation (power analysis)","Step 3: Randomization check — are groups balanced on key attributes?","Step 4: Primary analysis — t-test or proportion z-test","Step 5: Segment analysis — does effect vary by device/region/new_user","Step 6: Guardrail check — did revenue/session length stay stable","Step 7: Recommendation with business framing","Effect size (Cohen's d) for practical significance"],
    "keycode":["from scipy import stats\nfrom statsmodels.stats.proportion import proportions_ztest\nfrom statsmodels.stats.power import TTestIndPower\n\n# Step 1: Sample size calculation\npower_analysis = TTestIndPower()\nn = power_analysis.solve_power(effect_size=0.2, power=0.8, alpha=0.05)\nprint(f'Required sample size per group: {int(n)}')\n\n# Step 2: Check balance\nprint(df.groupby('variant')[['age','tenure','device_mobile']].mean())\n\n# Step 3: Proportion test for conversion rate\nconversions = df.groupby('variant')['converted'].agg(['sum','count'])\nstat, p = proportions_ztest(\n    conversions['sum'].values, conversions['count'].values\n)\n\n# Step 4: Full report\nfor grp in ['control', 'treatment']:\n    g = df[df['variant']==grp]\n    print(f'{grp}: n={len(g)}, cvr={g.converted.mean():.3%}, rev={g.revenue.mean():.2f}')"],
    "realworld":["Test a new recommendation algorithm's impact on order conversion rate","Evaluate whether a discount popup increases or harms LTV","Determine if a new onboarding flow increases Day-7 retention"],
    "interview":["Walk me through how you would design and analyze an A/B test from scratch.","How do you calculate required sample size before running an A/B test?","What are guardrail metrics and why are they important?"],
    "tasks":["Simulate an A/B test dataset and run the full analysis end-to-end","Calculate required sample size for a test targeting 5% lift in conversion at 80% power","Write a function ab_test_report() that takes control/treatment data and prints the full report"],
    "mistakes":["Stopping the test when it looks significant — multiple testing inflates false positive rate","Not checking if groups are balanced on key attributes before analysis","Ignoring guardrail metrics — a 5% conversion lift with 20% revenue drop is not a win"],
    "tips":["Pre-register your analysis plan before looking at results — prevents p-hacking","Segment every A/B result: does the effect hold for mobile? New users? All regions?","Report in business terms: '3.2% lift in checkout conversion = ₹42L additional annual revenue'"],
    "video":"https://www.youtube.com/results?search_query=A/B+testing+Python+scipy+statsmodels+tutorial"
  },
  { "name":"Linear regression and correlation analysis",
    "desc":"Model the relationship between variables and predict continuous outcomes.",
    "level":"int","must":True,
    "time":"3.5 hrs","order":4,
    "why":"Regression and correlation are fundamental tools for answering 'what drives this metric?' questions. Every business analyst eventually needs to answer: what factors predict revenue, churn, or NPS?",
    "concepts":["Pearson correlation: linear relationship (-1 to 1). Method='spearman' for non-linear","Correlation ≠ causation — always state this explicitly","Simple linear regression: y = mx + c","Multiple regression: y = b0 + b1*x1 + b2*x2 + ...","R²: proportion of variance explained (0-1)","Coefficient interpretation: 1 unit increase in x → β change in y","Residual analysis: should be random (no pattern)","sklearn: fit(X, y), predict(X), score(X, y)"],
    "keycode":["import pandas as pd, numpy as np\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nimport matplotlib.pyplot as plt\n\n# Correlation matrix\ncorr = df[['revenue','sessions','avg_order','tenure']].corr(method='pearson')\nprint(corr['revenue'].sort_values(ascending=False))\n\n# Simple linear regression\nX = df[['sessions']].values\ny = df['revenue'].values\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\n\nprint(f'Coefficient: {model.coef_[0]:.2f}')  # ₹ per session\nprint(f'Intercept: {model.intercept_:.2f}')\nprint(f'R² (test): {model.score(X_test, y_test):.3f}')  # variance explained"],
    "realworld":["What marketing channels most strongly predict revenue? (correlation analysis)","If we increase sessions by 10%, how much does revenue change? (regression coefficient)","Build a simple model to predict customer LTV from onboarding behavior"],
    "interview":["How do you interpret an R² of 0.7?","What is the difference between Pearson and Spearman correlation?","A regression coefficient is 5.2. What does that mean in plain English?"],
    "tasks":["Calculate correlation matrix for all numeric columns — which variables are most correlated with revenue?","Build a linear regression predicting revenue from sessions and marketing spend","Plot actual vs predicted values — does the model perform well?"],
    "mistakes":["Interpreting correlation as causation in a business recommendation","Using R² alone to evaluate model quality — check residual plots too","Not splitting train/test — evaluating on training data gives inflated R²"],
    "tips":["Correlation heatmap: sns.heatmap(df.corr()) should be your first EDA step for numeric data","Feature importance: which features have highest absolute correlation with target?","Always mention correlation ≠ causation when presenting regression-based insights"],
    "video":"https://www.youtube.com/results?search_query=linear+regression+correlation+python+sklearn+tutorial"
  },
]

PY_AUTOMATION = [
  { "name":"APIs with requests library: fetch, parse, handle pagination",
    "desc":"Pull data from any web API into a pandas DataFrame for analysis.",
    "level":"int","must":True,
    "time":"3 hrs","order":1,
    "why":"Modern data sources expose APIs. Weather data, financial data, social media metrics, internal product APIs — all are accessible via HTTP requests. This is how you get data that isn't in your database.",
    "concepts":["requests.get(url, params={}, headers={}) — GET request","r.status_code, r.raise_for_status() — error handling","r.json() — parse JSON response to Python dict","Pagination: loop while 'next' URL exists or page < max_page","Rate limiting: time.sleep() between requests","Authentication: headers={'Authorization': f'Bearer {token}'}","requests.Session for persistent connections"],
    "keycode":["import requests, pandas as pd, time\n\ndef fetch_all_pages(base_url, params, max_pages=10):\n    all_records = []\n    for page in range(1, max_pages+1):\n        params['page'] = page\n        r = requests.get(base_url, params=params,\n                        headers={'Authorization': f'Bearer {API_KEY}'})\n        r.raise_for_status()  # raise exception on 4xx/5xx\n        data = r.json()\n        records = data.get('results', [])\n        if not records:\n            break\n        all_records.extend(records)\n        time.sleep(0.1)  # rate limit courtesy\n    return pd.DataFrame(all_records)\n\ndf = fetch_all_pages('https://api.example.com/orders',\n                     params={'status': 'completed', 'per_page': 100})"],
    "realworld":["Pull weather data for 50 cities from OpenWeatherMap API","Fetch exchange rates from RBI API for currency conversion","Extract company reviews from a public API for sentiment analysis"],
    "interview":["How do you handle API pagination in Python?","How do you handle rate limiting gracefully?","How do you authenticate to a REST API using a Bearer token?"],
    "tasks":["Fetch data from a public API (e.g., OpenWeatherMap, CoinGecko) with pagination","Write a function that retries on failure with exponential backoff","Convert nested JSON API response to a flat pandas DataFrame"],
    "mistakes":["Not calling r.raise_for_status() — silently processes empty error responses","Not handling pagination — only getting the first page","Hardcoding API keys in code — use environment variables or .env files"],
    "tips":["Store API keys in .env file + python-dotenv — never in code committed to git","requests.Session() reuses TCP connection — faster for multiple requests to same host","json_normalize(data, record_path='items') flattens nested JSON to DataFrame"],
    "video":"https://www.youtube.com/results?search_query=python+requests+API+tutorial+pandas+data+analysis"
  },
  { "name":"Streamlit: build analyst self-service dashboards",
    "desc":"Turn a Python script into an interactive web dashboard in minutes — no web development needed.",
    "level":"adv","must":True,
    "time":"4 hrs","order":2,
    "why":"Streamlit is the fastest way to turn Python analysis into a tool stakeholders can use themselves. Build self-service dashboards that update with new data. This is a standout portfolio skill.",
    "concepts":["st.title(), st.header(), st.markdown() — text and headings","st.dataframe(df), st.table(df) — show DataFrames","st.plotly_chart(fig), st.pyplot(fig) — show charts","st.sidebar.selectbox(), st.sidebar.slider() — user inputs","st.metric(label, value, delta) — KPI cards","st.columns(3) — multi-column layout","@st.cache_data — cache expensive data loads","streamlit run app.py — local server; Streamlit Cloud for deployment"],
    "keycode":["import streamlit as st\nimport pandas as pd\nimport plotly.express as px\n\nst.set_page_config(page_title='Sales Dashboard', layout='wide')\nst.title('📊 Sales Analytics Dashboard')\n\n# Sidebar filters\nregion = st.sidebar.selectbox('Select Region', ['All'] + df['region'].unique().tolist())\ndate_range = st.sidebar.date_input('Date Range', value=(min_date, max_date))\n\n# Filter data\ndf_filtered = df.copy()\nif region != 'All':\n    df_filtered = df_filtered[df_filtered['region'] == region]\n\n# KPI cards\ncol1, col2, col3 = st.columns(3)\ncol1.metric('Total Revenue', f'₹{df_filtered.revenue.sum()/1e5:.1f}L',\n            delta=f'{pct_change:.1f}%')\n\n# Chart\nfig = px.line(df_filtered, x='month', y='revenue', color='region')\nst.plotly_chart(fig, use_container_width=True)"],
    "realworld":["Self-service sales dashboard for regional managers","Automated churn analysis tool: upload CSV, get insights instantly","HR headcount dashboard with department and grade filters"],
    "interview":["How is Streamlit different from a Jupyter Notebook for sharing analysis?","How do you add a date range filter and a dropdown to a Streamlit app?","How do you deploy a Streamlit app so stakeholders can access it?"],
    "tasks":["Build a 3-KPI-card + 2-chart sales dashboard with region filter using Streamlit","Add a file uploader so users can upload their own CSV and see automatic EDA","Deploy the app to Streamlit Community Cloud (free)"],
    "mistakes":["Not using @st.cache_data — reloads data on every user interaction, very slow","Not setting layout='wide' — charts are cramped in the default narrow layout","Heavy computation in the main script body — it reruns on every interaction"],
    "tips":["@st.cache_data on your data loading function — runs once, caches forever","st.session_state for maintaining state across interactions","Streamlit Community Cloud is free for public repos — perfect for portfolio projects"],
    "video":"https://www.youtube.com/results?search_query=streamlit+dashboard+tutorial+python+data+analyst"
  },
  { "name":"Automating reports: scheduling, Excel/PDF output, email",
    "desc":"Build scripts that run automatically and deliver formatted reports to stakeholders.",
    "level":"int","must":False,
    "time":"3 hrs","order":3,
    "why":"Manual monthly reports are a common analyst time sink. Automation scripts that run on a schedule and email stakeholders is a high-value, immediately demonstrable skill.",
    "concepts":["schedule library: schedule.every().monday.at('09:00').do(job)","openpyxl / xlsxwriter for formatted Excel reports","reportlab / weasyprint for PDF generation","smtplib + email.mime for sending email with attachment","subprocess.call(['python', 'script.py']) for system scheduler","environment variables for email credentials","Logging to file for headless script debugging"],
    "keycode":["import pandas as pd, schedule, time, smtplib\nfrom email.mime.multipart import MIMEMultipart\nfrom email.mime.base import MIMEBase\nfrom email import encoders\nimport xlsxwriter\n\ndef generate_report():\n    df = pd.read_sql(query, engine)\n    # Build Excel with formatting\n    with pd.ExcelWriter('report.xlsx', engine='xlsxwriter') as writer:\n        df.to_excel(writer, sheet_name='Data', index=False)\n        ws = writer.sheets['Data']\n        ws.set_column('A:Z', 15)\n    print('Report generated')\n\ndef send_email(filepath, recipients):\n    msg = MIMEMultipart()\n    msg['Subject'] = f'Monthly Report - {pd.Timestamp.now().strftime(\"%b %Y\")}'\n    with open(filepath, 'rb') as f:\n        part = MIMEBase('application', 'octet-stream')\n        part.set_payload(f.read())\n        encoders.encode_base64(part)\n        part.add_header('Content-Disposition', f'attachment; filename=report.xlsx')\n        msg.attach(part)\n    # send via SMTP...\n\nschedule.every().month.at('08:00').do(lambda: [generate_report(), send_email()])"],
    "realworld":["Automated weekly sales MIS emailed every Monday at 8am","Daily data quality check script that flags anomalies to Slack","Monthly P&L Excel report auto-generated and sent to CFO"],
    "interview":["How would you automate a report that currently takes 3 hours manually?","How do you schedule a Python script to run every Monday at 9am?","How do you send an email with an Excel attachment from Python?"],
    "tasks":["Build a script that generates a formatted Excel report from a SQL query","Add scheduling: run every weekday at 7am","Add email delivery with the report as an attachment"],
    "mistakes":["Hardcoding SMTP password in code — use environment variables or secrets manager","Not adding logging — when it fails at 3am, you won't know why without logs","Script dependencies on local paths — use absolute paths or config files"],
    "tips":["Use Windows Task Scheduler or cron (Linux/Mac) for system-level scheduling","openpyxl for reading existing Excel; xlsxwriter for creating new formatted reports","Wrap everything in try/except with logging — automated scripts run without supervision"],
    "video":"https://www.youtube.com/results?search_query=python+automate+excel+report+email+schedule+tutorial"
  },
]

# ─────────────────────────────────────────────
# BUILD THE HTML
# ─────────────────────────────────────────────

def esc(s):
    return (s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
             .replace('"','&quot;').replace("'","&#39;"))

def build_topic_card(t, sec, idx, item):
    tid = f"{t}_{sec}_{idx}"
    level_map = {"beg":"Beginner","int":"Intermediate","adv":"Advanced"}
    level_color = {"beg":"var(--green)","int":"var(--sql)","adv":"var(--red)"}
    level_bg = {"beg":"rgba(34,197,94,.1)","int":"rgba(245,158,11,.1)","adv":"rgba(239,68,68,.1)"}
    lbl = level_map.get(item["level"],"")
    lc = level_color.get(item["level"],"var(--text2)")
    lb = level_bg.get(item["level"],"transparent")
    time_str = item.get("time","")
    order_str = item.get("order","")
    video_url = item.get("video","")

    def li_list(items, bullet="›", color="var(--teal)"):
        out = ""
        for i in items:
            out += f'<li><span style="color:{color};font-weight:700;margin-right:6px">{bullet}</span>{esc(i)}</li>'
        return out

    def code_block(lines):
        return f'<div class="tc-code"><button class="copy-btn" onclick="copyCode(this)">Copy</button><code>{esc(lines)}</code></div>'

    codes = item.get("keycode",[])
    code_html = "".join(code_block(c) for c in codes) if codes else ""

    video_html = ""
    if video_url:
        video_html = f'''<div class="tc-section">
          <div class="tc-section-lbl">📺 Video Resource</div>
          <a href="{video_url}" target="_blank" style="display:inline-flex;align-items:center;gap:8px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.25);color:#f87171;padding:7px 14px;border-radius:var(--r3);font-size:12px;font-weight:700;text-decoration:none;margin-top:6px;">
            ▶ Watch Tutorial on YouTube ↗
          </a>
        </div>'''

    why_html = f'''<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px;">
      <div class="tc-why">
        <div class="tc-section-lbl">💡 Why It Matters</div>
        <p style="font-size:12.5px;color:var(--text2);line-height:1.7;margin-top:6px">{esc(item.get("why",""))}</p>
      </div>
      <div style="background:var(--surface2);border-radius:var(--r2);padding:14px;">
        <div class="tc-section-lbl">🎯 Key Concepts</div>
        <ul style="list-style:none;padding:0;margin-top:8px">{''.join(f"<li style='font-size:12px;color:var(--text2);padding:3px 0;border-bottom:1px solid var(--border)'>{esc(c)}</li>" for c in item.get("concepts",[]))}</ul>
      </div>
    </div>''' if item.get("why") else ""

    return f'''<div class="topic-card" id="tc-{tid}">
  <div class="topic-card-hdr" onclick="toggleCard(this)">
    <div class="tc-check-wrap">
      <div class="t-check {'done-check' if False else ''}" id="chk-{tid}" onclick="event.stopPropagation();toggleTopic('{tid}',this)"></div>
    </div>
    <div class="tc-hdr-body">
      <div class="tc-title">{esc(item["name"])}</div>
      <div class="tc-hdr-meta">
        {'<span class="tag tag-must">★ Must Know</span>' if item.get("must") else ""}
        <span class="tag" style="background:{lb};color:{lc}">{lbl}</span>
        {f'<span style="font-size:10px;color:var(--text3)">⏱ {time_str}</span>' if time_str else ""}
        {f'<span style="font-size:10px;color:var(--text3)">Order #{order_str}</span>' if order_str else ""}
      </div>
    </div>
    <div class="tc-arrow">▼</div>
  </div>
  <div class="topic-card-body">
    {why_html}
    {code_html}
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px;">
      <div>
        <div class="tc-section">
          <div class="tc-section-lbl">🌐 Real-World Use Cases</div>
          <ul class="tc-list">{''.join(f"<li>{esc(r)}</li>" for r in item.get("realworld",[]))}</ul>
        </div>
        <div class="tc-section" style="margin-top:12px">
          <div class="tc-section-lbl">📝 Practice Tasks</div>
          <ul class="tc-list tc-tasks">{''.join(f"<li>{esc(t_)}</li>" for t_ in item.get("tasks",[]))}</ul>
        </div>
      </div>
      <div>
        <div class="tc-section">
          <div class="tc-section-lbl">🎯 Interview Questions</div>
          <ul class="tc-list tc-iq">{''.join(f"<li>{esc(q)}</li>" for q in item.get("interview",[]))}</ul>
        </div>
        <div style="display:grid;grid-template-columns:1fr;gap:10px;margin-top:12px">
          {'<div class="tc-mistakes"><div class="tc-section-lbl" style="color:#f87171">⚠ Common Mistakes</div><ul class="tc-list">'+("".join(f"<li>{esc(m)}</li>" for m in item.get("mistakes",[])))+'</ul></div>' if item.get("mistakes") else ""}
          {'<div class="tc-tips"><div class="tc-section-lbl" style="color:#fbbf24">💡 Pro Tips</div><ul class="tc-list">'+("".join(f"<li>{esc(tp)}</li>" for tp in item.get("tips",[])))+'</ul></div>' if item.get("tips") else ""}
        </div>
      </div>
    </div>
    {video_html}
  </div>
</div>'''

# Read the existing v2 file
with open('/mnt/user-data/outputs/data_analyst_roadmap_v2.html', 'r') as f:
    content = f.read()

# Build the RICH_TOPICS JS object
all_rich = {
    "sql": {
        "basics": SQL_BASICS,
        "intermediate": SQL_INTERMEDIATE,
        "advanced": SQL_ADVANCED,
    },
    "py": {
        "basics": PY_BASICS,
        "pandas": PY_PANDAS,
        "viz": PY_VIZ,
        "stats": PY_STATS,
        "automation": PY_AUTOMATION,
    }
}

# Serialize rich topics as JS (we'll inject them)
rich_js = "const RICH_TOPICS = " + json.dumps(all_rich, ensure_ascii=False) + ";\n"

print("Rich topics JS size:", len(rich_js)//1024, "KB")
print("Content size:", len(content)//1024, "KB")
print("Done building data")

with open('/home/claude/rich_topics.js', 'w') as f:
    f.write(rich_js)
    
print("Saved rich_topics.js")
PYEOF
python3 /home/claude/build_roadmap.py
