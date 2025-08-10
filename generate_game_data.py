#!/usr/bin/env python3
"""
Google Feud Spanish Data Generator

This script reads seed queries from seed.json, gets Google autocomplete suggestions
for each query, and generates the game data files for each category.
"""

import json
import requests
import time
import random
from typing import Dict, List, Tuple
import urllib.parse
import os
from pathlib import Path

class GoogleAutocompleteClient:
    """Client for fetching Google autocomplete suggestions with rate limiting."""

    def __init__(self):
        self.base_url = "http://suggestqueries.google.com/complete/search"
        self.session = requests.Session()
        # Rotate user agents to appear more natural
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
        ]
        self.request_count = 0
        self.last_request_time = 0

    def get_suggestions(self, query: str, max_retries: int = 3, target_count: int = 10) -> List[str]:
        """Get autocomplete suggestions for a query with rate limiting and alphabet expansion."""

        all_suggestions = set()  # Use set to avoid duplicates

        # First, try the original query
        original_suggestions = self._fetch_suggestions(query, max_retries)
        for suggestion in original_suggestions:
            if suggestion != query.lower():
                all_suggestions.add(suggestion)

        print(f"    Original query gave {len(original_suggestions)} suggestions")

        # If we have enough suggestions, return them
        if len(all_suggestions) >= target_count:
            return list(all_suggestions)[:target_count]

        # Otherwise, try appending letters and numbers
        suffixes = list('abcdefghijklmnopqrstuvwxyz') + [str(i) for i in range(10)]

        for suffix in suffixes:
            if len(all_suggestions) >= target_count:
                break

            enhanced_query = f"{query} {suffix}"
            print(f"    Trying enhanced query: '{enhanced_query}'")

            enhanced_suggestions = self._fetch_suggestions(enhanced_query, max_retries)

            # Add new suggestions that start with our original query
            new_count = 0
            for suggestion in enhanced_suggestions:
                if (suggestion.lower().startswith(query.lower()) and
                    suggestion.lower() != query.lower() and
                    suggestion not in all_suggestions and
                    (len(suggestion) - len(query)) <= 50):  # Reasonable length limit
                    all_suggestions.add(suggestion)
                    new_count += 1

            if new_count > 0:
                print(f"      Added {new_count} new suggestions (total: {len(all_suggestions)})")

            # Small delay between enhanced queries
            time.sleep(random.uniform(1, 2))

        final_suggestions = list(all_suggestions)[:target_count]
        print(f"    Final result: {len(final_suggestions)} suggestions")
        return final_suggestions

    def _fetch_suggestions(self, query: str, max_retries: int = 3) -> List[str]:
        """Internal method to fetch suggestions for a single query."""

        # Rate limiting: wait between requests
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        min_delay = random.uniform(1.5, 3)  # Slightly faster for enhanced queries

        if time_since_last < min_delay:
            sleep_time = min_delay - time_since_last
            time.sleep(sleep_time)

        for attempt in range(max_retries):
            try:
                # Rotate user agent
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'application/json',
                    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }

                params = {
                    'client': 'firefox',
                    'q': query,
                    'hl': 'es',  # Spanish language
                    'gl': 'es',  # Spain geo-location
                    'output': 'json'
                }

                self.last_request_time = time.time()
                self.request_count += 1

                response = self.session.get(
                    self.base_url,
                    params=params,
                    headers=headers,
                    timeout=10
                )

                if response.status_code == 200:
                    content = response.text
                    if content.startswith('[') and content.endswith(']'):
                        data = json.loads(content)
                        suggestions = []
                        if len(data) > 1 and isinstance(data[1], list):
                            for item in data[1]:
                                if isinstance(item, str) and item.strip():
                                    clean_item = item.strip().lower()
                                    if clean_item != query.lower():
                                        suggestions.append(clean_item)

                        return suggestions

                elif response.status_code == 429:  # Too Many Requests
                    wait_time = (attempt + 1) * 10
                    print(f"      Rate limited, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue

                else:
                    print(f"      HTTP {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"      Request error: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 3
                    time.sleep(wait_time)

            except json.JSONDecodeError as e:
                print(f"      JSON decode error: {e}")
                break

            except Exception as e:
                print(f"      Unexpected error: {e}")
                break

        return []

def create_game_question(query: str, suggestions: List[str]) -> Dict:
    """Create a game question from a query and its suggestions."""

    # Filter and clean suggestions
    answers = []
    seen_completions = set()

    for suggestion in suggestions:
        # Remove the original query from the suggestion to get the completion
        completion = suggestion[len(query):].strip()

        # Clean up the completion
        completion = completion.strip(' .,;:!?-()[]{}"\'''""')

        if (len(completion) > 0 and
            completion.lower() not in seen_completions):

            answers.append({
                "text": completion,
                "rank": len(answers) + 1
            })
            seen_completions.add(completion.lower())

    return {
        "question": query,
        "answers": answers[:10]  # Limit to top 10
    }

def load_seed_data() -> Dict[str, List[str]]:
    """Load seed queries from seed.json."""

    with open('data/seed.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_category_data(category: str, questions: List[Dict]):
    """Save questions to category JSON file."""

    filename = f'data/{category}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(questions)} questions to {filename}")

def main():
    """Main function to generate game data."""

    print("🚀 Starting Google Feud Spanish data generation...")
    print("=" * 60)

    # Load seed data
    try:
        seed_data = load_seed_data()
        print(f"📖 Loaded seed data with {len(seed_data)} categories")
    except Exception as e:
        print(f"❌ Error loading seed data: {e}")
        return

    # Initialize Google client
    client = GoogleAutocompleteClient()

    # Process each category
    for category, queries in seed_data.items():
        print(f"\n📂 Processing category: {category}")
        print(f"   Queries to process: {len(queries)}")

        questions = []
        successful_queries = 0

        for i, query in enumerate(queries, 1):
            print(f"\n🔍 [{i}/{len(queries)}] Processing query: '{query}'")

            # Get suggestions with enhanced strategy
            suggestions = client.get_suggestions(query, target_count=10)

            if len(suggestions) >= 4:  # Need at least 4 for a good question
                # Create game question
                question = create_game_question(query, suggestions)

                if question and len(question['answers']) >= 4:
                    questions.append(question)
                    successful_queries += 1
                    print(f"    ✅ Created question with {len(question['answers'])} answers")
                else:
                    print(f"    ⚠️  Question created but insufficient valid answers")
            else:
                print(f"    ❌ Not enough suggestions found ({len(suggestions)})")

            # Extra delay after every 5 requests (since we're making more requests now)
            if client.request_count % 5 == 0:
                extra_delay = random.uniform(15, 25)
                print(f"    🛑 Taking extended break: {extra_delay:.1f} seconds...")
                time.sleep(extra_delay)

        # Save category data
        if questions:
            save_category_data(category, questions)
            print(f"✅ Category '{category}' completed: {successful_queries}/{len(queries)} successful")
        else:
            print(f"❌ No questions generated for category '{category}'")

        # Break between categories
        if category != list(seed_data.keys())[-1]:  # Not the last category
            break_time = random.uniform(30, 60)
            print(f"\n⏸️  Taking break before next category: {break_time:.1f} seconds...")
            time.sleep(break_time)

    print(f"\n🎉 Data generation completed!")
    print(f"📊 Total requests made: {client.request_count}")
    print("=" * 60)

if __name__ == "__main__":
    # Ensure we're in the right directory
    if not os.path.exists('data/seed.json'):
        print("❌ Error: seed.json not found. Please run from the project root directory.")
        exit(1)

    main()
