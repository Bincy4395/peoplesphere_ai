
function QuickActions() {
  const actions = [
    { id: 1, name: "Add Employee", icon: "👤" },
    { id: 2, name: "Add Department", icon: "🏢" },
    { id: 3, name: "Create Project", icon: "📁" },
    { id: 4, name: "View Reports", icon: "📊" }
  ]

  return (
    <div className="quick-actions">
      <h2>Quick Actions</h2>

      <div className="action-list">
        {actions.map((action) => (
          <button className="action-button" key={action.id}>
            <span>{action.icon}</span>
            {action.name}
          </button>
        ))}
      </div>
    </div>
  )
}

export default QuickActions
