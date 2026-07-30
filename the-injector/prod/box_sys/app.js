/* THE INJECTOR — force a letter through the wall (same-origin proxy) */
(function () {
  "use strict";

  const $ = (id) => document.getElementById(id);

  const SPEAKS_OK = [
    "The wire accepted the lie.",
    "Crate registered. Station will deny provenance.",
    "Forced delivery complete. They will open it anyway.",
    "Outside mark applied. Harassment en route.",
    "Import window closed on a package that was never shipped.",
  ];

  const SPEAKS_BAD = [
    "The wall refused the crate.",
    "Seal wrong · or the station is offline · or the wire is sulking.",
    "Delivery failed. Chester is not surprised.",
    "No. Try again when the terminal is actually running.",
  ];

  function pick(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function showResult(ok, text) {
    const el = $("result");
    el.hidden = false;
    el.className = "result " + (ok ? "ok" : "bad");
    el.textContent = text;
  }

  $("btn-clear").addEventListener("click", () => {
    $("from").value = "";
    $("subject").value = "";
    $("body").value = "";
    $("result").hidden = true;
  });

  $("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = $("btn");
    const token = ($("token").value || "").trim();
    const to = $("to").value;
    const from = ($("from").value || "").trim() || "unknown@outside.wire";
    const subject = ($("subject").value || "").trim() || "(no subject)";
    const body = $("body").value || "";
    // Optional advanced override; empty = server default (sdk-import :43101)
    const wire = ($("endpoint").value || "").trim();

    btn.disabled = true;
    btn.textContent = "…";

    const crate = {
      token: token,
      to: to,
      from: from,
      subject: subject,
      body: body,
    };
    if (wire) crate.wire = wire;

    try {
      // Same origin — injector server proxies to the terminal. Fixes CORS /
      // pywebview "fetch failed" when the UI tried to POST cross-port itself.
      const res = await fetch("/api/inject", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Mail-Token": token,
        },
        body: JSON.stringify(crate),
      });
      let data = null;
      try {
        data = await res.json();
      } catch (_e) {
        data = null;
      }
      if (!res.ok || !data || !data.ok) {
        const err =
          (data && data.error) || res.statusText || "unknown refusal";
        showResult(
          false,
          pick(SPEAKS_BAD) +
            "\n\n" +
            err +
            "\n\n(Start TERMINALS / sdk-import-station so mail inject is awake.)"
        );
        return;
      }
      const m = data.mail || {};
      showResult(
        true,
        pick(SPEAKS_OK) +
          "\n\n" +
          "id: " +
          (m.id || "?") +
          "\n" +
          "to: " +
          (m.to || to) +
          "\n" +
          "from: " +
          (m.from_label || from) +
          "\n" +
          "subject: " +
          (m.subject || subject) +
          "\n\n" +
          "Open MAIL on that station. It will say (outside)."
      );
    } catch (err) {
      showResult(
        false,
        pick(SPEAKS_BAD) +
          "\n\n" +
          (err && err.message ? err.message : String(err)) +
          "\n\nInjector glass itself failed — is this window's server alive?"
      );
    } finally {
      btn.disabled = false;
      btn.textContent = "PUSH";
    }
  });
})();
