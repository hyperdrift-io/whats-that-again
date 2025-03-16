<script lang="ts">
  import { onMount } from 'svelte';

  // State variables
  let query = '';
  let loading = false;
  let result = null;
  let sessionId = '';
  let tryNextModel = false;
  let searchHistory = [];
  let showSearchHistory = false;

  // Constants
  const CONFIDENCE_THRESHOLD = 0.4;

  // Handle search submission
  async function handleSearch() {
    if (!query.trim()) return;

    loading = true;

    try {
      const response = await fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: query.trim(),
          sessionId,
          tryNextModel
        })
      });

      if (!response.ok) {
        throw new Error('Search request failed');
      }

      const data = await response.json();

      // Reset the tryNextModel flag after use
      tryNextModel = false;

      // Store the result
      result = data;

      // Store session ID
      sessionId = data.sessionId;

      // Add to search history if not already in low confidence mode
      if (data.confidence >= CONFIDENCE_THRESHOLD && query.trim()) {
        addToSearchHistory(query.trim());
        query = ''; // Clear for new search
      }

      // Show search history for low confidence or when using "Not what you're looking for"
      showSearchHistory = data.confidence < CONFIDENCE_THRESHOLD || tryNextModel;

    } catch (error) {
      console.error('Error:', error);
      result = {
        answer: '<p class="error">An error occurred. Please try again.</p>',
        confidence: 0
      };
    } finally {
      loading = false;
    }
  }

  // Handle "Not what you're looking for?" button click
  function handleNotWhatYoureLookingFor() {
    // Set flag to try more powerful model
    tryNextModel = true;

    // Store current query in search history
    if (query.trim()) {
      addToSearchHistory(query.trim());
    }

    // Add prompt to help user provide more details
    query = query.trim()
      ? `${query}\n\nIt's not that. Here are more details: `
      : "It's not that. Here are more details: ";

    // Show search history
    showSearchHistory = true;
  }

  // Start a new search
  function startNewSearch() {
    // Reset session ID to start a fresh conversation
    sessionId = '';

    // Clear search input
    query = '';

    // Reset result
    result = null;

    // Hide search history
    showSearchHistory = false;

    // Reset flag
    tryNextModel = false;

    // Clear search history
    searchHistory = [];
  }

  // Add query to search history
  function addToSearchHistory(queryText) {
    // Add to history if not already present
    if (!searchHistory.includes(queryText)) {
      searchHistory = [...searchHistory, queryText];

      // Limit history items
      if (searchHistory.length > 10) {
        searchHistory = searchHistory.slice(-10);
      }
    }
  }

  // Auto-resize textarea
  function autoResize(event) {
    const textarea = event.target;
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
  }

  // Handle keyboard shortcuts
  function handleKeydown(event) {
    // Submit on Ctrl+Enter or Cmd+Enter
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
      event.preventDefault();
      handleSearch();
    }
    // Submit on Enter without shift
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSearch();
    }
  }
</script>

<main>
  <header>
    <h1>What's that again?</h1>
    <p class="tagline">Help you remember things on the tip of your tongue</p>
  </header>

  <div class="search-container">
    <textarea
      bind:value={query}
      placeholder="What are you trying to remember? Describe it in as much detail as you can..."
      on:input={autoResize}
      on:keydown={handleKeydown}
      class:hint-required={result && result.confidence < CONFIDENCE_THRESHOLD}
    ></textarea>

    <button
      on:click={handleSearch}
      class:hint-required={result && result.confidence < CONFIDENCE_THRESHOLD}
    >
      Search
    </button>
  </div>

  {#if loading}
    <div class="loader">
      <div class="loader-spinner"></div>
      <p>Searching your memory...</p>
    </div>
  {/if}

  {#if result}
    <div class="result-container">
      <h3>That thing you're thinking of is:</h3>
      <div class="answer" class:hint-required={result.confidence < CONFIDENCE_THRESHOLD}>
        {@html result.answer}
      </div>

      {#if result.usage_info}
        <div class="usage-info">{result.usage_info}</div>
      {/if}

      {#if result.memoryTags && result.memoryTags.length > 0}
        <div class="memory-tags">
          {#each result.memoryTags as tag}
            <span class="memory-tag">{tag}</span>
          {/each}
        </div>
      {/if}

      <div class="action-buttons">
        <button class="not-what-youre-looking-for" on:click={handleNotWhatYoureLookingFor}>
          Not what you're looking for?
        </button>

        <button class="new-search-button" on:click={startNewSearch}>
          New Search
        </button>
      </div>

      {#if showSearchHistory && searchHistory.length > 0}
        <div class="search-history">
          <h4>Your search journey:</h4>
          <div class="search-history-items">
            {#each searchHistory as item}
              <div class="search-history-item">{item}</div>
            {/each}
          </div>
        </div>
      {/if}
    </div>
  {/if}
</main>

<style>
  :global(:root) {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --background: #f9fafb;
    --card: #ffffff;
    --text: #111827;
    --text-light: #6b7280;
    --hint-required: #f97316;
    --hint-required-dark: #ea580c;
  }

  :global(*) {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

  :global(body) {
    background-color: var(--background);
    color: var(--text);
    line-height: 1.5;
    max-width: 640px;
    margin: 0 auto;
    padding: 1.5rem;
  }

  header {
    text-align: center;
    margin-bottom: 2rem;
  }

  h1 {
    color: var(--primary);
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }

  .tagline {
    color: var(--text-light);
    font-size: 1.1rem;
  }

  .search-container {
    position: relative;
    margin-bottom: 2rem;
  }

  textarea {
    width: 100%;
    padding: 1rem 1.25rem;
    border: 2px solid #e5e7eb;
    border-radius: 1rem;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    min-height: 80px;
    resize: vertical;
    font-family: inherit;
    line-height: 1.5;
    padding-right: 120px;
  }

  textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
  }

  textarea.hint-required {
    border-color: var(--hint-required);
    animation: nudge 0.5s ease;
  }

  textarea.hint-required:focus {
    box-shadow: 0 4px 12px rgba(249, 115, 22, 0.2);
  }

  button {
    position: absolute;
    right: 0.25rem;
    top: 0.25rem;
    border: none;
    background-color: var(--primary);
    color: white;
    border-radius: 1rem;
    padding: 0.6rem 1.5rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.3s ease;
    z-index: 10;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  button:hover {
    background-color: var(--primary-dark);
  }

  button.hint-required {
    background-color: var(--hint-required);
  }

  button.hint-required:hover {
    background-color: var(--hint-required-dark);
  }

  @keyframes nudge {
    0% { transform: translateX(0); }
    25% { transform: translateX(5px); }
    50% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
    100% { transform: translateX(0); }
  }

  .loader {
    text-align: center;
    margin: 2rem 0;
  }

  .loader-spinner {
    display: inline-block;
    width: 2.5rem;
    height: 2.5rem;
    border: 4px solid rgba(99, 102, 241, 0.2);
    border-radius: 50%;
    border-top-color: var(--primary);
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .result-container {
    background-color: var(--card);
    border-radius: 0.75rem;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border-left: 4px solid var(--primary);
    margin-bottom: 2rem;
    text-align: center;
  }

  .answer {
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--primary);
    margin: 1rem 0;
    padding: 0.75rem;
    background-color: #f3f4f6;
    border-radius: 0.5rem;
    word-break: break-word;
  }

  .answer.hint-required {
    color: var(--hint-required);
  }

  :global(.answer-link) {
    color: var(--primary);
    text-decoration: none;
    transition: all 0.2s ease;
    display: inline-block;
    position: relative;
  }

  :global(.answer-link:hover) {
    color: var(--primary-dark);
    text-decoration: underline;
  }

  :global(.answer-link::after) {
    content: "↗";
    font-size: 0.8em;
    margin-left: 0.3em;
    vertical-align: super;
  }

  .usage-info {
    margin-top: 1rem;
    font-size: 0.8rem;
    color: var(--text-light);
    text-align: center;
  }

  .memory-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1rem;
    justify-content: center;
  }

  .memory-tag {
    background-color: #dbeafe;
    color: #1e40af;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.8rem;
    display: inline-flex;
    align-items: center;
  }

  .memory-tag::before {
    content: "#";
    margin-right: 0.25rem;
    opacity: 0.7;
  }

  .action-buttons {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  .not-what-youre-looking-for {
    position: static;
    background-color: #f3f4f6;
    color: var(--text);
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 0.75rem 1.25rem;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .not-what-youre-looking-for:hover {
    background-color: #e5e7eb;
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .new-search-button {
    position: static;
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 0.5rem;
    padding: 0.75rem 1.25rem;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(99, 102, 241, 0.2);
  }

  .new-search-button:hover {
    background-color: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(99, 102, 241, 0.3);
  }

  .search-history {
    margin-top: 1rem;
    font-size: 0.85rem;
    color: var(--text-light);
    border-top: 1px solid #e5e7eb;
    padding-top: 0.75rem;
    max-height: 200px;
    overflow-y: auto;
  }

  .search-history h4 {
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }

  .search-history-item {
    padding: 0.5rem;
    border-radius: 0.25rem;
    margin-bottom: 0.5rem;
    background-color: #f3f4f6;
    color: var(--text);
  }

  :global(.low-confidence-prompt) {
    background-color: #fff3cd;
    border: 1px solid #ffecb5;
    border-radius: 0.5rem;
    padding: 1rem;
    margin: 1rem 0;
    text-align: left;
  }

  :global(.low-confidence-prompt p) {
    margin-bottom: 0.75rem;
  }

  :global(.low-confidence-prompt ul) {
    margin-left: 1.5rem;
    margin-bottom: 0.75rem;
  }

  :global(.hint-text) {
    font-style: italic;
    color: #856404;
    margin-top: 0.5rem;
  }
</style>
