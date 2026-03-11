import { fmtSize, fmtUptime, badgeClass } from '../utils'

function StatBar({ className, pct }) {
  return (
    <div className="stat-bar-wrap">
      <div className={`stat-bar ${className}`} style={{ width: pct + '%' }} />
    </div>
  )
}

function Badge({ className, children }) {
  return <span className={`stat-badge ${className}`}>{children}</span>
}

export default function StatsSection({ stats, updatedAt }) {
  if (!stats) {
    return (
      <>
        <div className="stats-grid">
          {['CPU', 'Memory', 'Disk', 'Network I/O', 'Uptime'].map(label => (
            <div key={label} className="stat-card">
              <div className="stat-header">
                <span className="stat-label">{label}</span>
              </div>
              <div className="stat-value">--</div>
            </div>
          ))}
        </div>
        <div className="stats-ts">{updatedAt}</div>
      </>
    )
  }

  const {
    cpu_percent, cpu_count, load_avg_1, load_avg_5, load_avg_15,
    ram_percent, ram_used_mb, ram_total_mb, ram_available_mb,
    disk_percent, disk_used_gb, disk_total_gb, disk_free_gb,
    net, process_count, uptime_seconds,
    gpus = [],
  } = stats

  return (
    <>
      <div className="stats-grid">
        {/* CPU */}
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">CPU</span>
            <Badge className={badgeClass(cpu_percent)}>{cpu_percent.toFixed(1)}%</Badge>
          </div>
          <div key={Math.floor(cpu_percent)} className="stat-value flash-val">{cpu_percent.toFixed(1)}%</div>
          <StatBar className="bar-cpu" pct={cpu_percent} />
          <div className="stat-sub">
            {cpu_count} cores &nbsp;|&nbsp; load avg: {load_avg_1} / {load_avg_5} / {load_avg_15}
          </div>
        </div>

        {/* Memory */}
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">Memory</span>
            <Badge className={badgeClass(ram_percent)}>{ram_percent.toFixed(1)}%</Badge>
          </div>
          <div key={Math.floor(ram_percent)} className="stat-value flash-val">{ram_percent.toFixed(1)}%</div>
          <StatBar className="bar-ram" pct={ram_percent} />
          <div className="stat-sub">
            {fmtSize(ram_used_mb)} used of {fmtSize(ram_total_mb)} &nbsp;|&nbsp; {fmtSize(ram_available_mb)} free
          </div>
        </div>

        {/* Disk */}
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">Disk</span>
            <Badge className={badgeClass(disk_percent)}>{disk_percent.toFixed(1)}%</Badge>
          </div>
          <div key={Math.floor(disk_percent)} className="stat-value flash-val">{disk_percent.toFixed(1)}%</div>
          <StatBar className="bar-disk" pct={disk_percent} />
          <div className="stat-sub">
            {disk_used_gb} GB used of {disk_total_gb} GB &nbsp;|&nbsp; {disk_free_gb} GB free
          </div>
        </div>

        {/* Network I/O */}
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">Network I/O</span>
            <Badge className="badge-info">Since boot</Badge>
          </div>
          <div className="net-row">
            <span className="net-lbl">↓ Received</span>
            <span className="net-val">{fmtSize(net.mb_recv)}</span>
          </div>
          <div className="net-row">
            <span className="net-lbl">↑ Sent</span>
            <span className="net-val">{fmtSize(net.mb_sent)}</span>
          </div>
          <div className="stat-sub">{process_count} processes running</div>
        </div>

        {/* Uptime */}
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">Uptime</span>
            <Badge className="badge-ok"><span className="pulse-dot" />Live</Badge>
          </div>
          <div className="uptime-val">{fmtUptime(uptime_seconds)}</div>
        </div>

        {/* GPUs */}
        {gpus.map(gpu => (
          <div key={gpu.index} className="stat-card gpu-card-wide">
            <div className="stat-header">
              <span className="stat-label">GPU {gpu.index}</span>
              <Badge className={badgeClass(gpu.load_percent)}>{gpu.load_percent.toFixed(1)}%</Badge>
            </div>
            <div className="stat-sub" style={{ marginTop: '-4px', marginBottom: '2px' }}>{gpu.name}</div>
            <div style={{ display: 'flex', gap: '1rem' }}>
              <div style={{ flex: 1 }}>
                <div className="stat-sub" style={{ marginBottom: '3px' }}>Utilization</div>
                <div key={Math.floor(gpu.load_percent)} className="stat-value flash-val">{gpu.load_percent.toFixed(1)}%</div>
                <div className="stat-bar-wrap" style={{ marginTop: '6px' }}>
                  <div className="stat-bar bar-gpu-load" style={{ width: gpu.load_percent + '%' }} />
                </div>
              </div>
              <div style={{ flex: 1 }}>
                <div className="stat-sub" style={{ marginBottom: '3px' }}>VRAM</div>
                <div key={Math.floor(gpu.memory_percent)} className="stat-value flash-val">{gpu.memory_percent.toFixed(1)}%</div>
                <div className="stat-bar-wrap" style={{ marginTop: '6px' }}>
                  <div className="stat-bar bar-gpu-mem" style={{ width: gpu.memory_percent + '%' }} />
                </div>
              </div>
            </div>
            <div className="stat-sub">
              {gpu.memory_used_mb.toFixed(0)} / {gpu.memory_total_mb.toFixed(0)} MB &nbsp;|&nbsp; {gpu.temperature_c} °C
            </div>
          </div>
        ))}
      </div>
      <div className="stats-ts">{updatedAt}</div>
    </>
  )
}
