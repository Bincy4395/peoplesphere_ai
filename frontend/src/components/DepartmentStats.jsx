
function DepartmentStats() {
  const departments = [
    { name: "Engineering", employees: 35 },
    { name: "Human Resources", employees: 12 },
    { name: "Finance", employees: 18 },
    { name: "Marketing", employees: 25 }
  ]

  return (
    <div className="department-section">
      <h2>Department Overview</h2>

      {departments.map((department) => (
        <div className="department-item" key={department.name}>
          <div className="department-info">
            <span>{department.name}</span>
            <span>{department.employees} Employees</span>
          </div>

          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${department.employees}%` }}
            ></div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default DepartmentStats
