
import { useState } from 'react'

function App() {
  const [employees, setEmployees] = useState([
    "Anu",
    "Rahul"
  ])

  const [employeeName, setEmployeeName] = useState("")
  const [editIndex, setEditIndex] = useState(null)

  function addEmployee() {
    if (employeeName.trim() === "") {
      alert("Please enter employee name")
      return
    }

    if (editIndex !== null) {
      const updatedEmployees = [...employees]
      updatedEmployees[editIndex] = employeeName.trim()

      setEmployees(updatedEmployees)
      setEditIndex(null)
    } else {
      setEmployees([...employees, employeeName.trim()])
    }

    setEmployeeName("")
  }

  function editEmployee(index) {
    setEmployeeName(employees[index])
    setEditIndex(index)
  }

  function deleteEmployee(index) {
    const updatedEmployees = employees.filter(
      (_, i) => i !== index
    )

    setEmployees(updatedEmployees)
  }

  return (
    <div>
      <h1>PeopleSphere AI</h1>

      <h2>{editIndex !== null ? "Edit Employee" : "Add Employee"}</h2>

      <input
        type="text"
        placeholder="Enter employee name"
        value={employeeName}
        onChange={(event) => setEmployeeName(event.target.value)}
      />

      <button onClick={addEmployee}>
        {editIndex !== null ? "Update Employee" : "Add Employee"}
      </button>

      <h2>Employee List</h2>

      <p>Total Employees: {employees.length}</p>

      {employees.map((employee, index) => (
        <div key={index}>
          <span>{employee}</span>

          <button onClick={() => editEmployee(index)}>
            Edit
          </button>

          <button onClick={() => deleteEmployee(index)}>
            Delete
          </button>
        </div>
      ))}
    </div>
  )
}

export default App
