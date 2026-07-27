/* THE INJECTOR — force a letter through the wall */
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
    const endpoint = ($("endpoint").value || "").trim();
    const token = ($("token").value || "").trim();
    const to = $("to").value;
    const from = ($("from").value || "").trim() || "unknown@outside.wire";
    const subject = ($("subject").value || "").trim() || "(no subject)";
    const body = $("body").value || "";

    if (!endpoint) {
      showResult(false, pick(SPEAKS_BAD) + "\n\nNo wire target.");
      return;
    }

    btn.disabled = true;
    btn.textContent = "PUSHING…";

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Mail-Token": token,
        },
        body: JSON.stringify({
          token: token,
          to: to,
          from: from,
          subject: subject,
          body: body,
        }),
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
            "\n\n(Is sdk-import-station / terminal mail online?)"
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
          "\n\nNetwork refused — start the terminal ROM first."
      );
    } finally {
      btn.disabled = false;
      btn.textContent = "FORCE DELIVERY";
    }
  });
})();
