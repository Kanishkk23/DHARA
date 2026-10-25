const riskZones = [
  {
    name: "Guwahati",
    level: "Critical",
    score: 87,
    rain: "142 mm",
    river: "5.82 m",
    status: "Rising",
  },
  {
    name: "Dibrugarh",
    level: "High",
    score: 74,
    rain: "118 mm",
    river: "4.91 m",
    status: "Rising",
  },
  {
    name: "Silchar",
    level: "Moderate",
    score: 58,
    rain: "86 mm",
    river: "3.74 m",
    status: "Stable",
  },
];

function ArrowUpRight() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M7 17 17 7" />
      <path d="M7 7h10v10" />
    </svg>
  );
}

function ChevronDown() {
  return (
    <svg
      width="15"
      height="15"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m6 9 6 6 6-6" />
    </svg>
  );
}

function BellIcon() {
  return (
    <svg
      width="19"
      height="19"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" />
      <path d="M13.73 21a2 2 0 0 1-3.46 0" />
    </svg>
  );
}

function CloudRainIcon() {
  return (
    <svg
      width="25"
      height="25"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M16 16.5a4 4 0 0 0-1-7.87A5 5 0 0 0 5.5 10.5 3.5 3.5 0 0 0 6 17h10" />
      <path d="M8 20v1" />
      <path d="M12 19v1" />
      <path d="M16 20v1" />
    </svg>
  );
}

function DropletsIcon() {
  return (
    <svg
      width="25"
      height="25"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M12 2.5s6 6.2 6 11a6 6 0 0 1-12 0c0-4.8 6-11 6-11Z" />
      <path d="M9 15.5a3 3 0 0 0 3 2.2" />
    </svg>
  );
}

function MapIcon() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m9 18-6 3V6l6-3 6 3 6-3v15l-6 3-6-3Z" />
      <path d="M9 3v15" />
      <path d="M15 6v15" />
    </svg>
  );
}

function ActivityIcon() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M3 12h4l3-8 4 16 3-8h4" />
    </svg>
  );
}

function ShieldIcon() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z" />
      <path d="m9 12 2 2 4-4" />
    </svg>
  );
}

function SettingsIcon() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06-1.8 1.8-.06-.06a1.7 1.7 0 0 0-1.88-.34 1.7 1.7 0 0 0-1.03 1.55V20h-2.55v-.09a1.7 1.7 0 0 0-1.03-1.55 1.7 1.7 0 0 0-1.88.34l-.06.06-1.8-1.8.06-.06A1.7 1.7 0 0 0 8.1 15a1.7 1.7 0 0 0-1.55-1.03H6V11.4h.55A1.7 1.7 0 0 0 8.1 10.37a1.7 1.7 0 0 0-.34-1.88L7.7 8.43l1.8-1.8.06.06a1.7 1.7 0 0 0 1.88.34A1.7 1.7 0 0 0 12.47 5.5V5h2.55v.5a1.7 1.7 0 0 0 1.03 1.53 1.7 1.7 0 0 0 1.88-.34l.06-.06 1.8 1.8-.06.06a1.7 1.7 0 0 0-.34 1.88 1.7 1.7 0 0 0 1.55 1.03H22v2.55h-.09A1.7 1.7 0 0 0 19.4 15Z" />
    </svg>
  );
}

export default function Home() {
  return (
    <main className="min-h-screen bg-[#07111f] text-white">
      <div className="flex min-h-screen">
        {/* Sidebar */}
        <aside className="hidden w-[248px] shrink-0 border-r border-white/[0.07] bg-[#091522] lg:flex lg:flex-col">
          <div className="flex h-[78px] items-center border-b border-white/[0.07] px-6">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-cyan-400 text-[#06111d] shadow-[0_0_25px_rgba(34,211,238,0.22)]">
                <svg
                  width="21"
                  height="21"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M12 3C9 7 6 10.5 6 14a6 6 0 0 0 12 0c0-3.5-3-7-6-11Z" />
                  <path d="M9.5 14.5a2.7 2.7 0 0 0 2.5 2" />
                </svg>
              </div>

              <div>
                <div className="text-[16px] font-semibold tracking-tight">
                  FloodFlash
                </div>
                <div className="text-[10px] uppercase tracking-[0.22em] text-slate-500">
                  Intelligence Platform
                </div>
              </div>
            </div>
          </div>

          <div className="px-4 pt-7">
            <div className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.2em] text-slate-600">
              Monitoring
            </div>

            <nav className="space-y-1">
              <a
                href="#"
                className="flex items-center gap-3 rounded-xl bg-cyan-400/[0.1] px-3 py-3 text-sm font-medium text-cyan-300"
              >
                <ActivityIcon />
                Overview
              </a>

              <a
                href="#"
                className="flex items-center gap-3 rounded-xl px-3 py-3 text-sm text-slate-400 transition hover:bg-white/[0.04] hover:text-white"
              >
                <MapIcon />
                Risk Map
              </a>

              <a
                href="#"
                className="flex items-center gap-3 rounded-xl px-3 py-3 text-sm text-slate-400 transition hover:bg-white/[0.04] hover:text-white"
              >
                <CloudRainIcon />
                Weather
              </a>

              <a
                href="#"
                className="flex items-center gap-3 rounded-xl px-3 py-3 text-sm text-slate-400 transition hover:bg-white/[0.04] hover:text-white"
              >
                <ShieldIcon />
                Alerts
              </a>
            </nav>

            <div className="mb-3 mt-9 px-3 text-[10px] font-semibold uppercase tracking-[0.2em] text-slate-600">
              System
            </div>

            <nav>
              <a
                href="#"
                className="flex items-center gap-3 rounded-xl px-3 py-3 text-sm text-slate-400 transition hover:bg-white/[0.04] hover:text-white"
              >
                <SettingsIcon />
                Settings
              </a>
            </nav>
          </div>

          <div className="mt-auto p-4">
            <div className="rounded-2xl border border-white/[0.07] bg-white/[0.025] p-4">
              <div className="mb-3 flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_10px_rgba(52,211,153,0.7)]" />
                <span className="text-xs font-medium text-emerald-300">
                  Systems operational
                </span>
              </div>

              <div className="text-[11px] leading-5 text-slate-500">
                Data services are connected and the monitoring engine is
                running.
              </div>
            </div>
          </div>
        </aside>

        {/* Main */}
        <section className="min-w-0 flex-1">
          {/* Header */}
          <header className="flex h-[78px] items-center justify-between border-b border-white/[0.07] px-5 sm:px-8">
            <div>
              <div className="text-xs text-slate-500">Flood monitoring</div>
              <h1 className="mt-1 text-lg font-semibold tracking-tight">
                Regional Overview
              </h1>
            </div>

            <div className="flex items-center gap-3">
              <button className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-white/[0.08] bg-white/[0.025] text-slate-400 transition hover:bg-white/[0.06] hover:text-white">
                <BellIcon />
                <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-cyan-400" />
              </button>

              <div className="hidden h-10 items-center gap-3 rounded-xl border border-white/[0.08] bg-white/[0.025] px-3 sm:flex">
                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-slate-700 text-[11px] font-semibold">
                  YK
                </div>
                <div className="text-xs">
                  <div className="font-medium text-slate-200">Operator</div>
                  <div className="text-[10px] text-slate-500">
                    Control center
                  </div>
                </div>
                <ChevronDown />
              </div>
            </div>
          </header>

          <div className="mx-auto max-w-[1500px] px-5 py-7 sm:px-8">
            {/* Hero */}
            <section className="relative overflow-hidden rounded-3xl border border-white/[0.08] bg-gradient-to-br from-[#0c2131] via-[#0b1a29] to-[#09131f] p-6 sm:p-8">
              <div className="pointer-events-none absolute -right-20 -top-32 h-80 w-80 rounded-full bg-cyan-400/[0.08] blur-3xl" />
              <div className="pointer-events-none absolute bottom-[-160px] left-[35%] h-80 w-80 rounded-full bg-blue-500/[0.06] blur-3xl" />

              <div className="relative z-10 flex flex-col justify-between gap-8 xl:flex-row xl:items-end">
                <div className="max-w-2xl">
                  <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-cyan-300/15 bg-cyan-300/[0.06] px-3 py-1.5 text-[11px] font-medium text-cyan-300">
                    <span className="h-1.5 w-1.5 rounded-full bg-cyan-300" />
                    LIVE RISK INTELLIGENCE
                  </div>

                  <h2 className="text-3xl font-semibold tracking-[-0.03em] text-white sm:text-4xl">
                    Flood risk,{" "}
                    <span className="text-cyan-300">before it arrives.</span>
                  </h2>

                  <p className="mt-4 max-w-xl text-sm leading-6 text-slate-400">
                    FloodFlash combines environmental signals, geographic
                    intelligence and predictive analytics to identify
                    emerging flood threats across monitored regions.
                  </p>
                </div>

                <div className="flex shrink-0 items-center gap-3">
                  <button className="rounded-xl border border-white/[0.09] bg-white/[0.04] px-4 py-2.5 text-xs font-medium text-slate-300 transition hover:bg-white/[0.08]">
                    View methodology
                  </button>

                  <button className="flex items-center gap-2 rounded-xl bg-cyan-300 px-4 py-2.5 text-xs font-semibold text-[#06111d] shadow-[0_8px_30px_rgba(34,211,238,0.15)] transition hover:bg-cyan-200">
                    Open risk map
                    <ArrowUpRight />
                  </button>
                </div>
              </div>
            </section>

            {/* Metrics */}
            <section className="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <div className="rounded-2xl border border-white/[0.07] bg-[#0b1826] p-5">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-500">
                    Monitored locations
                  </span>
                  <MapIcon />
                </div>

                <div className="mt-5 text-3xl font-semibold tracking-tight">
                  24
                </div>

                <div className="mt-2 text-[11px] text-emerald-400">
                  +4 locations this cycle
                </div>
              </div>

              <div className="rounded-2xl border border-white/[0.07] bg-[#0b1826] p-5">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-500">
                    Critical zones
                  </span>
                  <span className="h-2 w-2 rounded-full bg-red-400 shadow-[0_0_12px_rgba(248,113,113,0.6)]" />
                </div>

                <div className="mt-5 text-3xl font-semibold tracking-tight">
                  03
                </div>

                <div className="mt-2 text-[11px] text-red-300">
                  Immediate attention required
                </div>
              </div>

              <div className="rounded-2xl border border-white/[0.07] bg-[#0b1826] p-5">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-500">
                    Active alerts
                  </span>
                  <BellIcon />
                </div>

                <div className="mt-5 text-3xl font-semibold tracking-tight">
                  07
                </div>

                <div className="mt-2 text-[11px] text-amber-300">
                  2 escalated recently
                </div>
              </div>

              <div className="rounded-2xl border border-white/[0.07] bg-[#0b1826] p-5">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-500">
                    Prediction engine
                  </span>
                  <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.6)]" />
                </div>

                <div className="mt-5 text-3xl font-semibold tracking-tight">
                  98.4%
                </div>

                <div className="mt-2 text-[11px] text-emerald-400">
                  Model service operational
                </div>
              </div>
            </section>

            {/* Content grid */}
            <section className="mt-5 grid gap-5 xl:grid-cols-[1.55fr_1fr]">
              {/* Map */}
              <div className="overflow-hidden rounded-2xl border border-white/[0.07] bg-[#0b1826]">
                <div className="flex items-center justify-between border-b border-white/[0.07] px-5 py-4">
                  <div>
                    <h3 className="text-sm font-semibold">
                      Regional risk map
                    </h3>
                    <p className="mt-1 text-[11px] text-slate-500">
                      Current risk distribution across monitored areas
                    </p>
                  </div>

                  <button className="flex items-center gap-1.5 text-[11px] font-medium text-cyan-300">
                    Full map
                    <ArrowUpRight />
                  </button>
                </div>

                <div className="relative h-[360px] overflow-hidden bg-[#081421]">
                  {/* Stylized map background */}
                  <div className="absolute inset-0 opacity-40">
                    <div className="absolute left-[8%] top-[14%] h-px w-[78%] rotate-[18deg] bg-cyan-400/10" />
                    <div className="absolute left-[15%] top-[40%] h-px w-[68%] -rotate-[9deg] bg-cyan-400/10" />
                    <div className="absolute left-[5%] top-[65%] h-px w-[82%] rotate-[13deg] bg-cyan-400/10" />
                    <div className="absolute left-[22%] top-[25%] h-[70%] w-px rotate-[15deg] bg-cyan-400/10" />
                    <div className="absolute left-[54%] top-[5%] h-[90%] w-px -rotate-[12deg] bg-cyan-400/10" />
                    <div className="absolute left-[75%] top-[12%] h-[80%] w-px rotate-[21deg] bg-cyan-400/10" />
                  </div>

                  {/* Land silhouette */}
                  <div className="absolute left-[19%] top-[9%] h-[270px] w-[430px] rotate-[7deg] rounded-[45%_55%_40%_60%] border border-slate-500/10 bg-slate-400/[0.025] blur-[1px]" />

                  {/* Risk areas */}
                  <div className="absolute left-[54%] top-[31%] h-24 w-24 rounded-full bg-red-400/[0.08] blur-xl" />
                  <div className="absolute left-[53%] top-[30%] h-5 w-5 rounded-full border-2 border-red-300/80 bg-red-400 shadow-[0_0_22px_rgba(248,113,113,0.75)]" />

                  <div className="absolute left-[39%] top-[51%] h-20 w-20 rounded-full bg-orange-400/[0.07] blur-xl" />
                  <div className="absolute left-[38.5%] top-[50%] h-4 w-4 rounded-full border-2 border-orange-300/80 bg-orange-400 shadow-[0_0_20px_rgba(251,146,60,0.65)]" />

                  <div className="absolute left-[67%] top-[59%] h-20 w-20 rounded-full bg-yellow-300/[0.06] blur-xl" />
                  <div className="absolute left-[66.5%] top-[58%] h-4 w-4 rounded-full border-2 border-yellow-200/80 bg-yellow-300 shadow-[0_0_18px_rgba(253,224,71,0.55)]" />

                  <div className="absolute left-[56%] top-[27%] rounded-lg border border-white/[0.07] bg-[#0b1826]/90 px-2.5 py-1.5 backdrop-blur">
                    <div className="text-[10px] font-medium text-white">
                      Guwahati
                    </div>
                    <div className="mt-0.5 text-[9px] text-red-300">
                      Critical · 87
                    </div>
                  </div>

                  <div className="absolute left-[41%] top-[47%] rounded-lg border border-white/[0.07] bg-[#0b1826]/90 px-2.5 py-1.5 backdrop-blur">
                    <div className="text-[10px] font-medium text-white">
                      Dibrugarh
                    </div>
                    <div className="mt-0.5 text-[9px] text-orange-300">
                      High · 74
                    </div>
                  </div>

                  <div className="absolute left-[69%] top-[55%] rounded-lg border border-white/[0.07] bg-[#0b1826]/90 px-2.5 py-1.5 backdrop-blur">
                    <div className="text-[10px] font-medium text-white">
                      Silchar
                    </div>
                    <div className="mt-0.5 text-[9px] text-yellow-300">
                      Moderate · 58
                    </div>
                  </div>

                  <div className="absolute bottom-4 left-4 flex items-center gap-4 rounded-xl border border-white/[0.07] bg-[#091522]/90 px-3 py-2 backdrop-blur">
                    <div className="flex items-center gap-1.5 text-[9px] text-slate-400">
                      <span className="h-2 w-2 rounded-full bg-emerald-400" />
                      Low
                    </div>
                    <div className="flex items-center gap-1.5 text-[9px] text-slate-400">
                      <span className="h-2 w-2 rounded-full bg-yellow-300" />
                      Moderate
                    </div>
                    <div className="flex items-center gap-1.5 text-[9px] text-slate-400">
                      <span className="h-2 w-2 rounded-full bg-orange-400" />
                      High
                    </div>
                    <div className="flex items-center gap-1.5 text-[9px] text-slate-400">
                      <span className="h-2 w-2 rounded-full bg-red-400" />
                      Critical
                    </div>
                  </div>
                </div>
              </div>

              {/* Risk zones */}
              <div className="rounded-2xl border border-white/[0.07] bg-[#0b1826]">
                <div className="flex items-center justify-between border-b border-white/[0.07] px-5 py-4">
                  <div>
                    <h3 className="text-sm font-semibold">
                      Priority risk zones
                    </h3>
                    <p className="mt-1 text-[11px] text-slate-500">
                      Ranked by current risk score
                    </p>
                  </div>

                  <span className="rounded-lg border border-white/[0.07] px-2.5 py-1 text-[10px] text-slate-400">
                    Live
                  </span>
                </div>

                <div className="divide-y divide-white/[0.06]">
                  {riskZones.map((zone) => (
                    <div
                      key={zone.name}
                      className="px-5 py-4 transition hover:bg-white/[0.02]"
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="text-sm font-medium text-slate-200">
                            {zone.name}
                          </div>
                          <div className="mt-1 flex items-center gap-2 text-[10px] text-slate-500">
                            <span>{zone.rain} rainfall</span>
                            <span>•</span>
                            <span>River {zone.river}</span>
                          </div>
                        </div>

                        <div className="text-right">
                          <div
                            className={`text-lg font-semibold ${
                              zone.level === "Critical"
                                ? "text-red-300"
                                : zone.level === "High"
                                  ? "text-orange-300"
                                  : "text-yellow-300"
                            }`}
                          >
                            {zone.score}
                          </div>
                          <div className="text-[9px] uppercase tracking-wider text-slate-600">
                            Risk score
                          </div>
                        </div>
                      </div>

                      <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-white/[0.05]">
                        <div
                          className={`h-full rounded-full ${
                            zone.level === "Critical"
                              ? "w-[87%] bg-red-400"
                              : zone.level === "High"
                                ? "w-[74%] bg-orange-400"
                                : "w-[58%] bg-yellow-300"
                          }`}
                        />
                      </div>

                      <div className="mt-3 flex items-center justify-between">
                        <span
                          className={`text-[10px] font-medium ${
                            zone.level === "Critical"
                              ? "text-red-300"
                              : zone.level === "High"
                                ? "text-orange-300"
                                : "text-yellow-300"
                          }`}
                        >
                          {zone.level} risk
                        </span>

                        <span className="text-[10px] text-slate-600">
                          River {zone.status.toLowerCase()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>

            {/* Bottom intelligence row */}
            <section className="mt-5 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              <div className="rounded-2xl border border-white/[0.07] bg-[#0b1826] p-5">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-400/[0.08] text-cyan-300">
                    <CloudRainIcon />
                  </div>

                  <div>
                    <div className="text-sm font-medium">Rainfall signal</div>
                    <div className="text-[10px] text-slate-500">
                      Regional precipitation
                    </div>
                  </div>
                </div>

                <div className="mt-6 flex items-end justify-between">
                  <div>
                    <div className="text-2xl font-semibold">142 mm</div>
                    <div className="mt-1 text-[10px] text-slate-500">
                      Highest observed accumulation
                    </div>
                  </div>

                  <span className="text-xs text-red-300">↑ 18.6%</span>
                </div>
              </div>

              <div className="rounded-2xl border border-white/[0.07] bg-[#0b1826] p-5">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-400/[0.08] text-blue-300">
                    <DropletsIcon />
                  </div>

                  <div>
                    <div className="text-sm font-medium">Water levels</div>
                    <div className="text-[10px] text-slate-500">
                      Active river stations
                    </div>
                  </div>
                </div>

                <div className="mt-6 flex items-end justify-between">
                  <div>
                    <div className="text-2xl font-semibold">5.82 m</div>
                    <div className="mt-1 text-[10px] text-slate-500">
                      Peak monitored level
                    </div>
                  </div>

                  <span className="text-xs text-red-300">Rising</span>
                </div>
              </div>

              <div className="rounded-2xl border border-white/[0.07] bg-[#0b1826] p-5 md:col-span-2 xl:col-span-1">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-400/[0.08] text-emerald-300">
                    <ShieldIcon />
                  </div>

                  <div>
                    <div className="text-sm font-medium">System status</div>
                    <div className="text-[10px] text-slate-500">
                      FloodFlash intelligence
                    </div>
                  </div>
                </div>

                <div className="mt-6 flex items-end justify-between">
                  <div>
                    <div className="text-2xl font-semibold">Operational</div>
                    <div className="mt-1 text-[10px] text-slate-500">
                      Last synchronization: 2 min ago
                    </div>
                  </div>

                  <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 shadow-[0_0_14px_rgba(52,211,153,0.65)]" />
                </div>
              </div>
            </section>

            <footer className="mt-8 flex flex-col justify-between gap-2 border-t border-white/[0.06] pt-5 text-[10px] text-slate-600 sm:flex-row">
              <span>FloodFlash · Flood intelligence & early warning</span>
              <span>Prototype environment · Data engine initializing</span>
            </footer>
          </div>
        </section>
      </div>
    </main>
  );
}