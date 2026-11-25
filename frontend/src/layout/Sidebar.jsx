import { NavLink } from 'react-router-dom'

function Sidebar() {
  return (
    <aside className="sidebar">
      <h2 className="brand">PeopleSphere AI</h2>

      <p className="menu-title">MAIN MENU</p>

      <nav>
        <NavLink to="/" end className={({ isActive }) =>
          isActive ? "menu-item active" : "menu-item"
        }>
          Dashboard
        </NavLink>

        <NavLink to="/employees" className={({ isActive }) =>
          isActive ? "menu-item active" : "menu-item"
        }>
          Employees
        </NavLink>

        <NavLink to="/departments" className={({ isActive }) =>
          isActive ? "menu-item active" : "menu-item"
        }>
          Departments
        </NavLink>

        <NavLink to="/projects" className={({ isActive }) =>
          isActive ? "menu-item active" : "menu-item"
        }>
          Projects
        </NavLink>
      </nav>
    </aside>
  )
}

export default Sidebar