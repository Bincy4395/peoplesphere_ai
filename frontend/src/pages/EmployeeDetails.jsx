import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/api";

function EmployeeDetails() {
  const { id } = useParams();

  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function getEmployee() {
      try {
        const response = await api.get(`/employees/${id}`);
        setEmployee(response.data);
      } catch (error) {
        console.error(error);
        setError("Unable to load employee details");
      } finally {
        setLoading(false);
      }
    }

    getEmployee();
  }, [id]);

  if (loading) {
    return <div className="dashboard-content">Loading...</div>;
  }

  if (error) {
    return <div className="dashboard-content">{error}</div>;
  }

  if (!employee) {
    return <div className="dashboard-content">Employee not found</div>;
  }

  return (
    <div className="dashboard-content">
      <div className="employee-detail-header">
        <div>
          <h1>Employee Profile</h1>
          <p>Employee information and details</p>
        </div>

        <Link to="/employees" className="back-btn">
          Back to Employees
        </Link>
      </div>

      <div className="profile-card">
        <div className="profile-top">
          <div className="profile-avatar">{employee.name.charAt(0)}</div>

          <div>
            <h2>{employee.name}</h2>
            <p>{employee.designation}</p>
          </div>
        </div>

        <div className="profile-details">
          <div>
            <label>Employee ID</label>
            <p>{employee.id}</p>
          </div>

          <div>
            <label>Email</label>
            <p>{employee.email}</p>
          </div>

          <div>
            <label>Phone</label>
            <p>{employee.phone || "Not available"}</p>
          </div>

          <div>
            <label>Designation</label>
            <p>{employee.designation}</p>
          </div>

          <div>
            <label>Salary</label>
            <p>{employee.salary}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EmployeeDetails;
