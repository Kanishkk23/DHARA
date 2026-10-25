import React, { useState, useEffect, useRef, useMemo } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

/* =========================================================
   C-FLOOD BASINS & STATIONS DATASET (CWC & C-DAC NSM)
   Comprehensive CWC Water Level Sites & Discharge Sites
   ========================================================= */
const CFLOOD_BASINS = {
  "Beas & Satluj Basin (Himachal Pradesh)": {
    center: [32.239, 77.188],
    zoom: 11,
    stations: [
      { id: "kullu_gauge", name: "Kullu & Manali Beas Gauge", river: "Beas River", type: "water_level", lat: 32.239, lng: 77.188, level: 1211.20, danger: 1213.50, warning: 1212.00 },
      { id: "beas_discharge", name: "Pandoh Dam Outflow", river: "Beas River", type: "discharge", lat: 31.6700, lng: 77.0500, discharge: 4200, normalDischarge: 3400 },
      { id: "kinnaur_gauge", name: "Reckong Peo Satluj Site", river: "Satluj River", type: "water_level", lat: 31.650, lng: 78.475, level: 2281.40, danger: 2284.50, warning: 2282.00 },
      { id: "dharamsala_gauge", name: "Bhagsu Nag Hydro Station", river: "Manjhi Khad", type: "water_level", lat: 32.219, lng: 76.323, level: 1436.50, danger: 1439.00, warning: 1437.00 },
    ],
  },
  "Alaknanda & Mandakini Basin (Uttarakhand)": {
    center: [30.735, 79.066],
    zoom: 11,
    stations: [
      { id: "kedarnath_cwc", name: "Kedarnath Mandakini Site", river: "Mandakini River", type: "water_level", lat: 30.735, lng: 79.066, level: 3561.40, danger: 3564.50, warning: 3562.00 },
      { id: "chamoli_cwc", name: "Joshimath Alaknanda Site", river: "Alaknanda River", type: "water_level", lat: 30.556, lng: 79.567, level: 1871.20, danger: 1874.00, warning: 1872.00 },
      { id: "tapovan_discharge", name: "Tapovan Dam Outflow", river: "Dhauliganga", type: "discharge", lat: 30.495, lng: 79.620, discharge: 5100, normalDischarge: 4200 },
    ],
  },
  "Periyar & Kabini Basin (Kerala Hill Tracts)": {
    center: [11.554, 76.128],
    zoom: 11,
    stations: [
      { id: "wayanad_gauge", name: "Chooralmala Hydro Station", river: "Chaliyar / Kabini", type: "water_level", lat: 11.554, lng: 76.128, level: 846.80, danger: 849.00, warning: 847.00 },
      { id: "munnar_gauge", name: "Munnar Muthirapuzha Site", river: "Periyar Basin", type: "water_level", lat: 10.088, lng: 77.059, level: 1516.40, danger: 1519.50, warning: 1517.00 },
      { id: "idukki_discharge", name: "Idukki Spillway Outflow", river: "Periyar River", type: "discharge", lat: 9.850, lng: 76.970, discharge: 3900, normalDischarge: 3100 },
    ],
  },
  "Vashishti River Basin (Western Ghats)": {
    center: [17.532, 73.518],
    zoom: 11,
    stations: [
      { id: "chiplun_gauge", name: "Chiplun Town Bridge Site", river: "Vashishti River", type: "water_level", lat: 17.532, lng: 73.518, level: 15.80, danger: 18.00, warning: 16.50 },
      { id: "koyna_discharge", name: "Koyna Spillway Discharge", river: "Vashishti Headwaters", type: "discharge", lat: 17.400, lng: 73.750, discharge: 4600, normalDischarge: 3600 },
    ],
  },
  "Teesta River Basin (Sikkim Himalayas)": {
    center: [27.604, 88.647],
    zoom: 11,
    stations: [
      { id: "teesta_gauge", name: "Chungthang Confluence Site", river: "Teesta River", type: "water_level", lat: 27.604, lng: 88.647, level: 2731.80, danger: 2735.00, warning: 2732.50 },
      { id: "lachen_gauge", name: "Lachen High Altitude Gauge", river: "Lachen Chu", type: "water_level", lat: 27.720, lng: 88.555, level: 2790.00, danger: 2795.00, warning: 2792.00 },
    ],
  },
  "Jatinga Basin (Dima Hasao Hills)": {
    center: [25.176, 93.023],
    zoom: 11,
    stations: [
      { id: "haflong_gauge", name: "Haflong Valley River Site", river: "Jatinga / Kopili", type: "water_level", lat: 25.176, lng: 93.023, level: 496.80, danger: 499.50, warning: 497.00 },
    ],
  },
};

const STATE_MAPPING = {
  "Himachal Pradesh": "Beas & Satluj Basin (Himachal Pradesh)",
  "Uttarakhand": "Alaknanda & Mandakini Basin (Uttarakhand)",
  "Kerala Hill Tracts": "Periyar & Kabini Basin (Kerala Hill Tracts)",
  "Maharashtra Western Ghats": "Vashishti River Basin (Western Ghats)",
  "Sikkim Himalayas": "Teesta River Basin (Sikkim Himalayas)",
  "Assam & North-East Hills": "Jatinga Basin (Dima Hasao Hills)",
};

export default function CFloodEWS({ onBackToDashboard, currentSelectedCity }) {
  const [selectorTab, setSelectorTab] = useState("BY BASIN"); // "BY STATE" or "BY BASIN"
  const [selectedBasinKey, setSelectedBasinKey] = useState("Beas & Satluj Basin (Himachal Pradesh)");
  const [selectedStateKey, setSelectedStateKey] = useState("Himachal Pradesh");
  const [selectedStation, setSelectedStation] = useState(CFLOOD_BASINS["Beas & Satluj Basin (Himachal Pradesh)"].stations[0]);

    // Timeline forecast player
  const [forecastHour, setForecastHour] = useState(15); // 15m to 180m
  const [isPlaying, setIsPlaying] = useState(false);
  const playTimerRef = useRef(null);

  // Depth filter checkboxes
  const [showBelow05, setShowBelow05] = useState(true);
  const [showMid05to15, setShowMid05to15] = useState(true);
  const [showAbove15, setShowAbove15] = useState(true);
  const [showWaterLevelSites, setShowWaterLevelSites] = useState(true);
  const [showDischargeSites, setShowDischargeSites] = useState(true);

  // Map refs
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);
  const markersLayerRef = useRef(null);
  const inundationLayerRef = useRef(null);
  const [mouseCoords, setMouseCoords] = useState('20° 28\' 14" N 85° 52\' 20" E');

  const currentBasin = useMemo(() => {
    return CFLOOD_BASINS[selectedBasinKey] || CFLOOD_BASINS["Mahanadi Basin"];
  }, [selectedBasinKey]);

  // Sync if dashboard city changed
  useEffect(() => {
    if (!currentSelectedCity) return;
    const matchedStateBasin = STATE_MAPPING[currentSelectedCity.name] || STATE_MAPPING["Odisha"];
    if (matchedStateBasin && CFLOOD_BASINS[matchedStateBasin]) {
      setSelectedBasinKey(matchedStateBasin);
    }
  }, [currentSelectedCity]);

  // Dynamic forecast date text (advances with hour scrub)
  const currentForecastDate = useMemo(() => {
    const base = new Date(2026, 7, 28, 6, 0); // 28/8/2026 6:00 hrs
    base.setHours(base.getHours() + forecastHour);
    const d = base.getDate();
    const m = base.getMonth() + 1;
    const y = base.getFullYear();
    const h = String(base.getHours()).padStart(2, "0");
    return `${d}/${m}/${y} ${h}:00 hrs`;
  }, [forecastHour]);

  // Play / Pause loop
  useEffect(() => {
    if (isPlaying) {
      playTimerRef.current = setInterval(() => {
        setForecastHour((prev) => {
          if (prev >= 72) return 0;
          return prev + 3;
        });
      }, 700);
    } else {
      if (playTimerRef.current) clearInterval(playTimerRef.current);
    }
    return () => {
      if (playTimerRef.current) clearInterval(playTimerRef.current);
    };
  }, [isPlaying]);

  // Initialize Leaflet Map
  useEffect(() => {
    if (!mapContainerRef.current || mapRef.current) return;

    const map = L.map(mapContainerRef.current, {
      center: currentBasin.center,
      zoom: currentBasin.zoom,
      zoomControl: true,
      attributionControl: true,
    });

    L.tileLayer(
      "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
      {
        attribution: "Tiles &copy; Esri, CWC, C-DAC Supercomputing Grid",
        maxZoom: 18,
      }
    ).addTo(map);

    inundationLayerRef.current = L.layerGroup().addTo(map);
    markersLayerRef.current = L.layerGroup().addTo(map);

    map.on("mousemove", (e) => {
      const lat = e.latlng.lat.toFixed(4);
      const lng = e.latlng.lng.toFixed(4);
      setMouseCoords(`${lat}° N  ${lng}° E`);
    });

    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  // Update center when basin changes
  useEffect(() => {
    if (!mapRef.current) return;
    mapRef.current.flyTo(currentBasin.center, currentBasin.zoom, { duration: 1.2 });
  }, [currentBasin]);

  // Render stations and dynamic inundation polygons based on 72h forecast scrub
  useEffect(() => {
    if (!mapRef.current || !markersLayerRef.current || !inundationLayerRef.current) return;

    markersLayerRef.current.clearLayers();
    inundationLayerRef.current.clearLayers();

    // 1. Inundation Polygons (CWC depth tiers)
    // Scale factor increases with forecastHour
    const growth = 1 + (forecastHour / 72) * 0.55;

    currentBasin.stations.forEach((st) => {
      // 0 to 0.5m layer (Yellow)
      if (showBelow05) {
        L.circle([st.lat, st.lng], {
          radius: 3500 * growth,
          color: "#eab308",
          fillColor: "#facc15",
          fillOpacity: 0.28,
          weight: 1.5,
        }).addTo(inundationLayerRef.current);
      }

      // 0.5m to 1.5m layer (Orange)
      if (showMid05to15) {
        L.circle([st.lat, st.lng], {
          radius: 2200 * growth,
          color: "#f97316",
          fillColor: "#fb923c",
          fillOpacity: 0.35,
          weight: 1.8,
        }).addTo(inundationLayerRef.current);
      }

      // Above 1.5m layer (Red - Deep Flood Surge)
      if (showAbove15 && forecastHour >= 24) {
        L.circle([st.lat, st.lng], {
          radius: 1200 * (forecastHour / 72),
          color: "#ef4444",
          fillColor: "#f87171",
          fillOpacity: 0.45,
          weight: 2,
        }).addTo(inundationLayerRef.current);
      }

      // 2. Station Markers
      if (st.type === "water_level" && showWaterLevelSites) {
        const yellowPin = L.divIcon({
          className: "cwc-water-pin",
          html: `<div style="position: relative; width: 26px; height: 26px; display: grid; place-items: center;">
                   <div style="width: 22px; height: 22px; border-radius: 50% 50% 50% 0; background: #eab308; border: 2px solid #fff; transform: rotate(-45deg); box-shadow: 0 2px 6px rgba(0,0,0,0.5);"></div>
                   <div style="position: absolute; top: 5px; width: 6px; height: 6px; border-radius: 50%; background: #fff;"></div>
                 </div>`,
          iconSize: [26, 26],
          iconAnchor: [13, 24],
        });

        L.marker([st.lat, st.lng], { icon: yellowPin })
          .bindPopup(
            `<div style="font-family: inherit; font-size: 12px; padding: 4px;">
               <span style="font-size: 10px; font-weight: 800; color: #ca8a04; text-transform: uppercase;">CWC Water Level Gauging Site</span>
               <strong style="display: block; font-size: 14px; margin: 2px 0;">${st.name}</strong>
               <div>River: <strong>${st.river}</strong></div>
               <div>Current Stage: <strong style="color: #0284c7;">${st.level} m</strong></div>
               <div>Warning Level: <strong>${st.warning} m</strong></div>
               <div>Danger Level: <strong style="color: #dc2626;">${st.danger} m</strong></div>
               <div style="margin-top: 4px; font-size: 11px; color: #16a34a; font-weight: 700;">Forecast at ${currentForecastDate}: +${((forecastHour / 72) * 0.45).toFixed(2)}m</div>
             </div>`
          )
          .addTo(markersLayerRef.current);
      } else if (st.type === "discharge" && showDischargeSites) {
        const bluePin = L.divIcon({
          className: "cwc-discharge-pin",
          html: `<div style="position: relative; width: 26px; height: 26px; display: grid; place-items: center;">
                   <div style="width: 22px; height: 22px; border-radius: 50% 50% 50% 0; background: #0284c7; border: 2px solid #fff; transform: rotate(-45deg); box-shadow: 0 2px 6px rgba(0,0,0,0.5);"></div>
                   <div style="position: absolute; top: 5px; width: 6px; height: 6px; border-radius: 50%; background: #fff;"></div>
                 </div>`,
          iconSize: [26, 26],
          iconAnchor: [13, 24],
        });

        L.marker([st.lat, st.lng], { icon: bluePin })
          .bindPopup(
            `<div style="font-family: inherit; font-size: 12px; padding: 4px;">
               <span style="font-size: 10px; font-weight: 800; color: #0284c7; text-transform: uppercase;">CWC / GloFAS Discharge Site</span>
               <strong style="display: block; font-size: 14px; margin: 2px 0;">${st.name}</strong>
               <div>River: <strong>${st.river}</strong></div>
               <div>Current Discharge: <strong style="color: #0284c7;">${st.discharge.toLocaleString()} m³/s</strong></div>
               <div>Normal Discharge: <strong>${st.normalDischarge.toLocaleString()} m³/s</strong></div>
               <div style="margin-top: 4px; font-size: 11px; color: #ca8a04; font-weight: 700;">Forecast Discharge (${currentForecastDate}): ${Math.round(st.discharge * growth).toLocaleString()} m³/s</div>
             </div>`
          )
          .addTo(markersLayerRef.current);
      }
    });
  }, [
    currentBasin,
    forecastHour,
    showBelow05,
    showMid05to15,
    showAbove15,
    showWaterLevelSites,
    showDischargeSites,
    currentForecastDate,
  ]);

  return (
    <div className="cflood-container">
      {/* =========================================================
          C-FLOOD OFFICIAL GOVERNMENT TOP BAR
          ========================================================= */}
      <header className="cflood-topbar">
        <div className="cflood-brand-group">
          <div className="cflood-logo-badge">C-Flood</div>
          <div className="cflood-titles">
            <span className="cflood-title-main">EARLY WARNING SYSTEM</span>
            <span className="cflood-title-sub">FOR FLOOD PREDICTION</span>
          </div>
        </div>

        <div className="cflood-nav-links">
          <div className="cflood-ticker">
            <span className="ticker-badge">Alerts</span>
            <span>Rapid Mountain Flash Flood Early Warning Model Active · NDRF & CWC Real-Time Telemetry</span>
          </div>

          <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
            <button className="cflood-switch-btn" onClick={onBackToDashboard}>
              ⚡ Command Dashboard →
            </button>
          </div>
        </div>
      </header>

      {/* =========================================================
          MAP AREA & FLOATING SELECTION CONTROLS
          ========================================================= */}
      <div className="cflood-map-wrapper">
        <div ref={mapContainerRef} className="cflood-map-element" />

        {/* LEFT FLOATING CONTROL PANEL: SELECT STATION */}
        <div className="cflood-station-card">
          <div className="cflood-station-header">
            <span>Select Station</span>
            <span style={{ fontSize: "11px", color: "#64748b" }}>▲</span>
          </div>

          {/* DUAL TABS: BY STATE | BY BASIN */}
          <div className="cflood-tabs-row">
            <button
              className={`cflood-tab-btn ${selectorTab === "BY STATE" ? "active" : ""}`}
              onClick={() => setSelectorTab("BY STATE")}
            >
              BY STATE
            </button>
            <button
              className={`cflood-tab-btn ${selectorTab === "BY BASIN" ? "active" : ""}`}
              onClick={() => setSelectorTab("BY BASIN")}
            >
              BY BASIN
            </button>
          </div>

          <div className="cflood-selectors-body">
            {selectorTab === "BY STATE" ? (
              <>
                <div className="cflood-select-group">
                  <label>Select State</label>
                  <select
                    value={selectedStateKey}
                    onChange={(e) => {
                      setSelectedStateKey(e.target.value);
                      const b = STATE_MAPPING[e.target.value] || "Mahanadi Basin";
                      setSelectedBasinKey(b);
                      setSelectedStation(CFLOOD_BASINS[b].stations[0]);
                    }}
                  >
                    {Object.keys(STATE_MAPPING).map((st) => (
                      <option key={st} value={st}>{st}</option>
                    ))}
                  </select>
                </div>

                <div className="cflood-select-group">
                  <label>Station Select</label>
                  <select
                    value={selectedStation?.id || ""}
                    onChange={(e) => {
                      const stations = currentBasin?.stations || [];
                      const st = stations.find((s) => s.id === e.target.value);
                      if (st) {
                        setSelectedStation(st);
                        mapRef.current?.flyTo([st.lat, st.lng], 13, { duration: 1 });
                      }
                    }}
                  >
                    {(currentBasin?.stations || []).map((st) => (
                      <option key={st.id} value={st.id}>
                        {st.name} ({st.type === "water_level" ? "Water Level" : "Discharge"})
                      </option>
                    ))}
                  </select>
                </div>
              </>
            ) : (
              <>
                <div className="cflood-select-group">
                  <label>Select River Basin</label>
                  <select
                    value={selectedBasinKey}
                    onChange={(e) => {
                      setSelectedBasinKey(e.target.value);
                      if (CFLOOD_BASINS[e.target.value]?.stations?.length > 0) {
                        setSelectedStation(CFLOOD_BASINS[e.target.value].stations[0]);
                      }
                    }}
                  >
                    {Object.keys(CFLOOD_BASINS).map((b) => (
                      <option key={b} value={b}>{b}</option>
                    ))}
                  </select>
                </div>

                <div className="cflood-select-group">
                  <label>Station Select</label>
                  <select
                    value={selectedStation?.id || ""}
                    onChange={(e) => {
                      const stations = currentBasin?.stations || [];
                      const st = stations.find((s) => s.id === e.target.value);
                      if (st) {
                        setSelectedStation(st);
                        mapRef.current?.flyTo([st.lat, st.lng], 13, { duration: 1 });
                      }
                    }}
                  >
                    {(currentBasin?.stations || []).map((st) => (
                      <option key={st.id} value={st.id}>
                        {st.name} ({st.type === "water_level" ? "Water Level" : "Discharge"})
                      </option>
                    ))}
                  </select>
                </div>
              </>
            )}
          </div>
        </div>

        {/* RIGHT FLOATING LEGEND (EXACT CWC C-FLOOD STYLE) */}
        <div className="cflood-legend-card">
          <div className="legend-header">
            <strong>Legend</strong>
            <span style={{ fontSize: "11px", color: "#64748b" }}>▲</span>
          </div>

          <div className="legend-list">
            <label className="legend-row">
              <input
                type="checkbox"
                checked={showBelow05}
                onChange={(e) => setShowBelow05(e.target.checked)}
              />
              <span className="legend-box yellow" />
              <span>Below 0.5 m</span>
            </label>

            <label className="legend-row">
              <input
                type="checkbox"
                checked={showMid05to15}
                onChange={(e) => setShowMid05to15(e.target.checked)}
              />
              <span className="legend-box orange" />
              <span>0.5 m - 1.5 m</span>
            </label>

            <label className="legend-row">
              <input
                type="checkbox"
                checked={showAbove15}
                onChange={(e) => setShowAbove15(e.target.checked)}
              />
              <span className="legend-box red" />
              <span>Above 1.5 m</span>
            </label>

            <label className="legend-row">
              <input
                type="checkbox"
                checked={showWaterLevelSites}
                onChange={(e) => setShowWaterLevelSites(e.target.checked)}
              />
              <span className="pin-symbol yellow">📍</span>
              <span>Water Level Sites</span>
            </label>

            <label className="legend-row">
              <input
                type="checkbox"
                checked={showDischargeSites}
                onChange={(e) => setShowDischargeSites(e.target.checked)}
              />
              <span className="pin-symbol blue">📍</span>
              <span>Discharge Sites</span>
            </label>
          </div>

          <div className="legend-lang-row">
            <select style={{ width: "100%", padding: "4px 8px", fontSize: "11.5px", borderRadius: "4px", border: "1px solid #cbd5e1" }}>
              <option>English 🌐</option>
              <option>Hindi (हिंदी)</option>
            </select>
          </div>

          <div className="legend-badge-row">
            <span className="gov-badge blue">C-DAC</span>
            <span className="gov-badge cyan">NRSC</span>
            <span className="gov-badge dark">CWC</span>
          </div>
        </div>

        {/* BOTTOM RAPID MOUNTAIN FLASH FLOOD LEAD-TIME MONITOR */}
        <div className="cflood-timeline-player">
          <div className="timeline-top-meta">
            <div className="timeline-timestamp-box" style={{ color: "#d4b996" }}>
              ⚡ RAPID FLASH FLOOD LEAD-TIME: +{forecastHour} MINS ({forecastHour <= 30 ? "SURGE IMMINENT" : forecastHour <= 60 ? "CREST WAVE" : "RUNOFF DRAINAGE"})
            </div>
            <div className="timeline-coords-box">
              {mouseCoords}
            </div>
          </div>

          <div className="timeline-controls-row">
            <button
              className="player-btn play"
              onClick={() => setIsPlaying(!isPlaying)}
              title={isPlaying ? "Pause Simulation" : "Run Surge Simulation (15m - 180m)"}
              style={{ background: "#c25e40", color: "#fff" }}
            >
              {isPlaying ? "⏸" : "▶"}
            </button>

            <div className="scrubber-track-container">
              <input
                type="range"
                min="15"
                max="180"
                step="15"
                value={forecastHour}
                onChange={(e) => setForecastHour(Number(e.target.value))}
                className="cflood-slider"
              />
              <div className="days-label-row">
                <span style={{ color: "#ef4444" }}>15 min (Surge Arrival)</span>
                <span style={{ color: "#e59840" }}>45 min (Gorge Crest)</span>
                <span style={{ color: "#d4b996" }}>90 min (Watershed Peak)</span>
                <span style={{ color: "#7ea193" }}>180 min (Recession)</span>
              </div>
            </div>

            <button
              className="player-btn reset"
              onClick={() => {
                setForecastHour(15);
                setIsPlaying(false);
              }}
              title="Reset Lead Time"
            >
              ⟲
            </button>
          </div>

          <div className="timeline-footer-caption" style={{ color: "#d4b996" }}>
            Hydrodynamic mountain surge wave model &middot; Manning velocity 4.8 m/s &middot; High Alert Danger Zones and Safe Havens Active.
          </div>
        </div>
      </div>

      {/* =========================================================
          OFFICIAL GOVERNMENT PARTNERS FOOTER
          ========================================================= */}
      <footer className="cflood-gov-footer">
        <div className="partner-credits">
          <span>🇮🇳 <strong>Make in India</strong></span>
          <span>⚡ <strong>C-DAC</strong></span>
          <span>🌊 <strong>Ministry of Jal Shakti</strong></span>
          <span>🛰️ <strong>NRSC / ISRO</strong></span>
          <span>💻 <strong>MeitY</strong></span>
          <span>🏢 <strong>National Supercomputing Mission</strong></span>
        </div>
        <div className="nsm-disclaimer">
          Developed by C-DAC under National Supercomputing Mission in association with Central Water Commission (CWC)
        </div>
      </footer>

      </div>
  );
}
