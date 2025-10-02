#!/usr/bin/env python3
"""
Simple LinkedIn Job Scraper
Scrapes LinkedIn job postings and extracts job details.
"""

import requests
from bs4 import BeautifulSoup
import yaml
import time
import random
import json
from fake_useragent import UserAgent

def load_config():
    """Load configuration from YAML file."""
    with open('config2.yaml', 'r') as file:
        return yaml.safe_load(file)

def get_random_headers():
    """Generate random headers to avoid detection."""
    ua = UserAgent()
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def fetch_page(url):
    """Fetch a web page with random headers."""
    headers = get_random_headers()
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_job_links(config):
    """Get job links from LinkedIn search for multiple job titles."""
    job_titles = config['job_search']['job_titles']
    location = config['job_search']['location']
    max_results = config['job_search'].get('max_results', 10)

    all_job_links = []

    # loop over relavent job titles and identify associated openings
    for job_title in job_titles:
        print(f"Searching for: {job_title}")
        search_url = f"https://www.linkedin.com/jobs/search?keywords={job_title}&location={location}"

        # return the page of linked in results, or 
        # continue to the next job title if none exists
        soup = fetch_page(search_url)
        if not soup:
            continue

        # Find job links - simplified selector
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/jobs/view/' in href:
                if href.startswith('/'):
                    href = f"https://www.linkedin.com{href}"
                if href not in all_job_links:
                    all_job_links.append(href)

        # Add delay between searches
        time.sleep(random.uniform(1, 2))

    # Limit total results
    return all_job_links[:max_results]

def extract_job_details(job_url):
    """Extract job details from a single job page."""
    print(f"Extracting: {job_url}")

    soup = fetch_page(job_url)
    if not soup:
        return {
            'job_url': job_url,
            'job_name': 'Failed to fetch',
            'company': 'Failed to fetch',
            'job_description': 'Failed to fetch',
            'additional_info': 'Could not access page'
        }

    # Extract job title/name
    job_name = ""
    title_selectors = ['h1', '.top-card-layout__title'
                       , '.job-details-jobs-unified-top-card__job-title', 'title']
    
    for selector in title_selectors:
        element = soup.select_one(selector)
        if element:
            text = element.get_text(strip=True)
            # Clean up common prefixes/suffixes and take relevant part
            if len(text) > 5 and 'linkedin' not in text.lower():
                job_name = text.split('|')[0].split('-')[0].strip()  # Take first part before separators
                break

    # Extract company name
    company = ""
    company_selectors = [
        '.job-details-jobs-unified-top-card__company-name',
        '.jobs-unified-top-card__company-name',
        '.top-card-layout__second-subline',
        '.job-details-jobs-unified-top-card__primary-description-container a',
        'a[data-tracking-control-name="job_details_topcard_company_url"]'
    ]

    for selector in company_selectors:
        element = soup.select_one(selector)
        if element:
            text = element.get_text(strip=True)
            if len(text) > 1 and 'linkedin' not in text.lower():
                # Clean up company name - remove location and other metadata
                company = text.split('Charlotte, NC')[0].split(' ago')[0].split(' applicants')[0].strip()
                if company:
                    break

    # If no company found in selectors, try to extract from URL or page title
    if not company:
        # Try to extract from URL pattern
        if '-at-' in job_url:
            url_parts = job_url.split('-at-')
            if len(url_parts) > 1:
                company_part = url_parts[1].split('-')[0]
                company = company_part.replace('-', ' ').title()

    # Extract description - look for job-specific content
    description = ""

    # Try common job description selectors first
    for selector in ['.show-more-less-html__markup', '.jobs-description__content', '.job-description']:
        element = soup.select_one(selector)
        if element:
            description = element.get_text(strip=True)
            break

    # Fallback: find text containing job-related keywords
    if not description:
        job_keywords = ['responsibilities', 'requirements', 'experience',
                         'skills', 'qualifications', 'position', 'role','duties']
        for element in soup.find_all(['div', 'section']):
            text = element.get_text(strip=True).lower()
            if len(text) > 300 and any(keyword in text for keyword in job_keywords):
                description = element.get_text(strip=True)
                break

    # TO DO 
    # CLEAN UP JOB DESCRIPTION FURTHER, FIGURE OUT HOW TO REMOVE BOILERPLATE TEXT AND ONLY 
    # INCLUDE INFORMATION SPECIFIC ABOUT THE JOB, NOT THE COMPANY!

    # Extract compensation info - simplified
    compensation = "No compensation info found"
    page_text = soup.get_text().lower()
    if '$' in page_text:
        # Look for salary patterns
        for word in page_text.split():
            if '$' in word and any(char.isdigit() for char in word):
                compensation = f"{word}"
                break

    return {
        'job_url': job_url,
        'job_name': job_name or 'No title found',
        'company': company or 'No company found',
        'job_description': description or 'No description found',
        'additional_info': compensation
    }

def scrape_jobs():
    """Main scraping function."""
    config = load_config()

    job_titles = config['job_search']['job_titles']
    location = config['job_search']['location']
    print(f"Searching for {len(job_titles)} job types in {location}")
    print(f"Job titles: {', '.join(job_titles)}")

    # Get job links
    job_links = get_job_links(config)
    print(f"Found {len(job_links)} job links")

    if not job_links:
        return []

    # Extract details for each job
    job_details = []
    for i, job_url in enumerate(job_links, 1):
        print(f"Processing job {i}/{len(job_links)}")
        details = extract_job_details(job_url)
        job_details.append(details)

        # Random delay to be polite
        if i < len(job_links):
            time.sleep(random.uniform(1, 3))

    return job_details

def save_results(job_details):
    """Save results to JSON file."""
    with open('job_results.json', 'w', encoding='utf-8') as f:
        json.dump(job_details, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(job_details)} jobs to job_results.json")

def main():
    """Main function."""
    try:
        job_details = scrape_jobs()

        if job_details:
            print(f"\nFound {len(job_details)} jobs:")
            for i, job in enumerate(job_details, 1):
                print(f"\n{i}. {job['job_name']} at {job['company']}")
                print(f"   URL: {job['job_url']}")
                print(f"   Description: {job['job_description'][:100]}...")
                print(f"   Info: {job['additional_info']}")

            save_results(job_details)
            return job_details
        else:
            print("No jobs found")
            return []

    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    main()