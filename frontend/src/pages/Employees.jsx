import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api/api";

function Employees() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function getEmployees() {
      try {
        const response = await api.get("/employees");
        setEmployees(response.data);
      } catch (error) {
        console.error(error);
        setError("Unable to load employees");
      } finally {
        setLoading(false);
      }
    }

    getEmployees();
  }, []);

  if (loading) {
    return <div className="dashboard-content">Loading employees...</div>;
  }

  if (error) {
    return <div className="dashboard-content">{error}</div>;
  }

  return (
    <div className="dashboard-content">
      <div className="employee-page-header">
        <div>
          <h1>Employees</h1>
          <p>Manage your workforce and employee details.</p>
        </div>

        <button className="add-employee-btn">+ Add Employee</button>
      </div>

      <div className="employee-list">
        <div className="employee-list-header">
          <h2>All Employees</h2>
          <span>{employees.length} Employees</span>
        </div>

        <table>
          <thead>
            <tr>
              <th>Employee ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Designation</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {employees.map((employee) => (
              <tr key={employee.id}>
                <td>EMP00{employee.id}</td>

                <td>
                  <Link
                    className="employee-name-link"
                    to={`/employees/${employee.id}`}
                  >
                    {employee.name}
                  </Link>
                </td>

                <td>{employee.email}</td>

                <td>{employee.designation}</td>

                <td>
                  <Link
                    className="view-details-btn"
                    to={`/employees/${employee.id}`}
                  >
                    View Details
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {employees.length === 0 && <p>No employees found.</p>}
      </div>
    </div>
  );
}

export default Employees;
