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
        {#if result.answer}
          <a href="https://search.brave.com/search?q={encodeURIComponent(result.answer)}" target="_blank" rel="noopener noreferrer">
            {@html result.answer}
          </a>
        {:else}
          {@html result.answer}
        {/if}
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
