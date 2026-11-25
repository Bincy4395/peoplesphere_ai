
function ProjectProgress() {
  const projects = [
    {
      id: 1,
      name: "Employee Management System",
      status: "In Progress",
      progress: 75
    },
    {
      id: 2,
      name: "Payroll Automation",
      status: "In Progress",
      progress: 50
    },
    {
      id: 3,
      name: "HR Analytics",
      status: "Completed",
      progress: 100
    }
  ]

  return (
    <div className="project-section">
      <h2>Project Progress</h2>

      {projects.map((project) => (
        <div className="project-item" key={project.id}>
          <div className="project-info">
            <span>{project.name}</span>
            <span>{project.progress}%</span>
          </div>

          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${project.progress}%` }}
            ></div>
          </div>

          <p className="project-status">{project.status}</p>
        </div>
      ))}
    </div>
  )
}

export default ProjectProgress
