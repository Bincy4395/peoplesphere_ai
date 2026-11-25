
function RecentEmployees() {
  const employees = [
    {
      id: 1,
      name: "Anu",
      designation: "Software Developer",
      department: "Engineering",
      status: "Active"
    },
    {
      id: 2,
      name: "Rahul",
      designation: "HR Executive",
      department: "Human Resources",
      status: "Active"
    },
    {
      id: 3,
      name: "Sneha",
      designation: "Accountant",
      department: "Finance",
      status: "On Leave"
    },
    {
      id: 4,
      name: "Arun",
      designation: "UI Designer",
      department: "Marketing",
      status: "Active"
    }
  ]

  return (
    <div className="recent-employees">
      <h2>Recent Employees</h2>

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Designation</th>
            <th>Department</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {employees.map((employee) => (
            <tr key={employee.id}>
              <td>{employee.name}</td>
              <td>{employee.designation}</td>
              <td>{employee.department}</td>
              <td>{employee.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default RecentEmployees
