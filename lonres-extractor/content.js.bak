(function () {
  if (!window.location.href.includes("page_size=50")) {
    console.log("LonRes Extractor: URL does not contain page_size=50");
    return;
  }

  const scripts = document.querySelectorAll("script");
  if (scripts.length === 0) {
    console.log("LonRes Extractor: No script tags found.");
    return;
  }

  const lastScript = scripts[scripts.length - 1].textContent;
  try {
    const jsonStart = lastScript.indexOf('{');
    const jsonText = lastScript.slice(jsonStart);
    const data = JSON.parse(jsonText);

    const results = data?.props?.pageProps?.dehydratedState?.queries?.[0]?.state?.data?.results;
    if (results) {
      console.log("LonRes Extractor: Sending results to Render API...");

      fetch("https://lonres-activity-monitor.onrender.com/receive", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ results: results })
      })
      .then(response => {
        if (response.ok) {
          console.log("LonRes Extractor: Results successfully sent to Render API.");
        } else {
          console.error("LonRes Extractor: Failed to send results. Status:", response.status);
        }
      })
      .catch(error => {
        console.error("LonRes Extractor: Error sending results to Render API:", error);
      });

    } else {
      console.log("LonRes Extractor: Results not found in JSON structure.");
    }
  } catch (e) {
    console.error("LonRes Extractor: Failed to parse JSON from script tag.", e);
  }
})();
