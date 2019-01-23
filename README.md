# Shul Scraper
- Python code to scrape weekly schedule info from local synagogue's website and email to list of recipients.
## Components
1. Code is packaged with Python package requirements into AWS Lambda deployment package.
2. Lambda function scrapes website, formats text into HTML, and sends to email recipients.
3. AWS Cloudwatch cronjob automates weekly pull.
