/* Medicare enrollment window engine. Pure functions, no Date-object month math,
   so there are no timezone or DST surprises. Runs in the browser and in Node.
   Rules: docs/enrollment-calculator-spec.md (verified September 2026). */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.IEP = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var MONTHS = ["January","February","March","April","May","June","July",
                "August","September","October","November","December"];

  /* ---- month arithmetic on {y, m} with m in 1..12 ---- */
  function addMonths(ym, n) {
    var idx = ym.y * 12 + (ym.m - 1) + n;
    return { y: Math.floor(idx / 12), m: (idx % 12) + 1 };
  }
  function cmp(a, b) { return (a.y * 12 + a.m) - (b.y * 12 + b.m); }   // months apart
  function daysIn(y, m) { return new Date(Date.UTC(y, m, 0)).getUTCDate(); }
  function first(ym) { return { y: ym.y, m: ym.m, d: 1 }; }
  function last(ym)  { return { y: ym.y, m: ym.m, d: daysIn(ym.y, ym.m) }; }
  function fmtMonth(ym) { return MONTHS[ym.m - 1] + " " + ym.y; }
  function fmtDate(d)   { return MONTHS[d.m - 1] + " " + d.d + ", " + d.y; }
  function iso(d) {
    return d.y + "-" + String(d.m).padStart(2, "0") + "-" + String(d.d).padStart(2, "0");
  }

  /* ---- input validation ---- */
  function validateDOB(dob, today) {
    if (!dob || !Number.isInteger(dob.y) || !Number.isInteger(dob.m) || !Number.isInteger(dob.d))
      return "Please enter the month, day, and year you were born.";
    if (dob.m < 1 || dob.m > 12) return "The month needs to be between 1 and 12.";
    if (dob.y < 1900 || dob.y > today.y) return "Please check the year. It should be four digits, like 1961.";
    if (dob.d < 1 || dob.d > daysIn(dob.y, dob.m))
      return MONTHS[dob.m - 1] + " " + dob.y + " only has " + daysIn(dob.y, dob.m) + " days. Please check the day.";
    var age = ageOn(dob, today);
    if (age < 0) return "That date is in the future. Please check the year.";
    if (age > 110) return "Please check the year. It should be four digits, like 1961.";
    return null;
  }
  function ageOn(dob, on) {
    var a = on.y - dob.y;
    if (on.m < dob.m || (on.m === dob.m && on.d < dob.d)) a--;
    return a;
  }

  /* ---- the core rule ----
     Medicare entitlement begins the first day of the month you turn 65. If you were
     born on the 1st, entitlement begins the first day of the month BEFORE your
     birthday month (SSA treats you as attaining an age the day before your birthday).
     The 7-month Initial Enrollment Period is the 3 months before that month, the
     month itself, and the 3 months after. */
  function eligibilityMonth(dob) {
    var bm = { y: dob.y + 65, m: dob.m };
    return dob.d === 1 ? addMonths(bm, -1) : bm;
  }

  /* Coverage start if you sign up during month `enroll` of the IEP (rules since 2023). */
  function coverageStartIfEnrolled(enroll, elig) {
    var diff = cmp(enroll, elig);
    if (diff < 0) return first(elig);                 // before your 65th month: starts that month
    return first(addMonths(enroll, 1));                // in or after it: the month after you sign up
  }

  /* Next General Enrollment Period (Jan 1 to Mar 31) on or after `today`. */
  function nextGEP(today) {
    var y = (today.m <= 3) ? today.y : today.y + 1;
    return { start: { y: y, m: 1, d: 1 }, end: { y: y, m: 3, d: 31 } };
  }

  /* ---- main ----
     input: { dob:{y,m,d}, today:{y,m,d},
              benefits: "none" | "retirement" | "disability" | "unsure",
              working:  "no" | "yes" | "unsure",
              employerSize: "20plus" | "under20" | "unsure" | null,
              hsa: "yes" | "no" | "unsure" | null }               */
  function compute(input) {
    var dob = input.dob, today = input.today;
    var err = validateDOB(dob, today);
    if (err) return { error: err };

    var age = ageOn(dob, today);
    var elig = eligibilityMonth(dob);
    var iepStart = addMonths(elig, -3), iepEnd = addMonths(elig, 3);
    var todayYM = { y: today.y, m: today.m };
    var monthsToOpen = cmp(iepStart, todayYM);          // >0 future, <=0 open or past
    var monthsPastEnd = cmp(todayYM, iepEnd);            // >0 closed

    var status = monthsToOpen > 0 ? "upcoming" : (monthsPastEnd > 0 ? "closed" : "open");
    var monthsLeft = status === "open" ? (cmp(iepEnd, todayYM) + 1) : 0;

    var tiles = [];
    for (var i = -3; i <= 3; i++) {
      var m = addMonths(elig, i);
      tiles.push({
        ym: m, label: fmtMonth(m),
        phase: i < 0 ? "early" : (i === 0 ? "birthday" : "late"),
        coverage: coverageStartIfEnrolled(m, elig),
        isNow: cmp(m, todayYM) === 0
      });
    }

    var partBStartIfOnTime = first(elig);
    var medigapStart = elig, medigapEnd = addMonths(elig, 5);

    var r = {
      age: age,
      bornOnFirst: dob.d === 1,
      turns65: { y: dob.y + 65, m: dob.m },
      elig: elig,
      iep: { start: first(iepStart), end: last(iepEnd), startYM: iepStart, endYM: iepEnd },
      bestBy: last(addMonths(elig, -1)),                  // sign up by end of the month before
      onTimeCoverage: partBStartIfOnTime,
      medigap: { start: first(medigapStart), end: last(medigapEnd) },
      status: status, monthsToOpen: monthsToOpen, monthsLeft: monthsLeft,
      tiles: tiles,
      path: "standard",
      flags: []
    };

    /* ---- routing ---- */
    var b = input.benefits || "none";
    var w = input.working || "no";

    if (b === "disability" && age < 65) {
      r.path = "disability";
      return r;
    }
    if (w === "yes") {
      r.path = "working";
      r.employerSize = input.employerSize || "unsure";
      r.hsa = input.hsa || "unsure";
      if (r.employerSize === "under20") r.flags.push("under20");
      if (r.hsa === "yes") r.flags.push("hsa");
      if (b === "retirement" || b === "disability") r.flags.push("autoEnrolledWhileWorking");
    } else if (b === "retirement" || (b === "disability" && age >= 65)) {
      r.path = "auto";
      r.cardArrives = first(addMonths(elig, -3));
    } else {
      r.path = "standard";
      if (w === "unsure") r.flags.push("workingUnsure");
    }
    if (b === "unsure") r.flags.push("benefitsUnsure");

    if (status === "closed" && r.path === "standard") {
      r.path = "late";
      r.gep = nextGEP(today);
      var full12 = Math.floor(Math.max(0, cmp(todayYM, iepEnd) - 1) / 12);
      r.fullYearsLate = full12;
    }
    if (r.path === "working") {
      // SEP: 8 months beginning the month after employment or coverage ends. Illustrate.
      r.sepLengthMonths = 8;
    }
    return r;
  }

  /* ---- calendar file (three reminders) ---- */
  function icsFor(r) {
    function stamp(d) { return iso(d).replace(/-/g, ""); }
    function ev(uid, d, title, desc) {
      var next = new Date(Date.UTC(d.y, d.m - 1, d.d + 1));
      var nd = { y: next.getUTCFullYear(), m: next.getUTCMonth() + 1, d: next.getUTCDate() };
      return ["BEGIN:VEVENT", "UID:" + uid + "@bluegrassmedicarehelp.com",
              "DTSTAMP:20260916T120000Z",
              "DTSTART;VALUE=DATE:" + stamp(d), "DTEND;VALUE=DATE:" + stamp(nd),
              "SUMMARY:" + title, "DESCRIPTION:" + desc.replace(/\n/g, "\\n"),
              "END:VEVENT"].join("\r\n");
    }
    var lines = ["BEGIN:VCALENDAR", "VERSION:2.0",
                 "PRODID:-//Bluegrass Medicare Help//Enrollment Window//EN", "CALSCALE:GREGORIAN"];
    lines.push(ev("iep-open", r.iep.start, "Medicare enrollment window opens",
      "Your 7-month Initial Enrollment Period starts today. Signing up this month means coverage starts " +
      fmtDate(r.onTimeCoverage) + ". Questions: Bluegrass Medicare Help, (859) 618-6443."));
    lines.push(ev("iep-best", r.bestBy, "Last day to sign up for on-time Medicare coverage",
      "Sign up by today so Part A and Part B start " + fmtDate(r.onTimeCoverage) +
      ". Bluegrass Medicare Help, (859) 618-6443."));
    lines.push(ev("iep-close", r.iep.end, "Medicare enrollment window closes",
      "Your Initial Enrollment Period ends today. After this, late penalties can apply. " +
      "Bluegrass Medicare Help, (859) 618-6443."));
    lines.push("END:VCALENDAR");
    return lines.join("\r\n") + "\r\n";
  }

  return {
    compute: compute, validateDOB: validateDOB, ageOn: ageOn,
    eligibilityMonth: eligibilityMonth, coverageStartIfEnrolled: coverageStartIfEnrolled,
    nextGEP: nextGEP, addMonths: addMonths, daysIn: daysIn,
    fmtMonth: fmtMonth, fmtDate: fmtDate, iso: iso, icsFor: icsFor, MONTHS: MONTHS
  };
});
