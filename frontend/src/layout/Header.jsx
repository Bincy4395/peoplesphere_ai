
function Header() {
  return (
    <header className="header">

      <input
        type="text"
        placeholder="Search employees, projects..."
      />

      <div className="profile">
        <span>🔔</span>
        <span>Admin</span>
      </div>

    </header>
  )
}

export default Header
