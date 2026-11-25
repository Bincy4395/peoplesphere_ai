import { useState, useEffect } from "react";

function EmployeeApiTest() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function getEmployees() {
      try {
        const response = await fetch("http://localhost:8000/employees");

        if (!response.ok) {
          throw new Error("Failed to fetch employees");
        }

        const data = await response.json();

        setEmployees(data);
      } catch (error) {
        console.error("API Error:", error);
      } finally {
        setLoading(false);
      }
    }

    getEmployees();
  }, []);

  if (loading) {
    return <p>Loading employees...</p>;
  }

  return (
    <div>
      <h2>Employees from API</h2>

      {employees.map((employee) => (
        <p key={employee.id}>{employee.name}</p>
      ))}
    </div>
  );
}

export default EmployeeApiTest;
