import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import api from "../api/api";

function EditEmployee() {
  const { id } = useParams();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [departments, setDepartments] = useState([]);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    designation: "",
    salary: "",
    department_id: "",
  });

  useEffect(() => {
    async function getEmployee() {
      try {
        const response = await api.get(`/employees/${id}`);

        setFormData(response.data);
      } catch (error) {
        console.error(error);
        setError("Unable to load employee details");
      } finally {
        setLoading(false);
      }
    }

    getEmployee();
  }, [id]);

  useEffect(() => {
    async function getDepartments() {
      try {
        const response = await api.get("/departments");
        setDepartments(response.data);
      } catch (error) {
        console.error("Error fetching departments:", error);
      }
    }

    getDepartments();
  }, []);

  if (loading) {
    return <div className="dashboard-content">Loading...</div>;
  }

  if (error) {
    return <div className="dashboard-content">{error}</div>;
  }

  function handleChange(e) {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }

  return (
    <div className="dashboard-content">
      <h1>Edit Employee</h1>
      <p>Update employee information.</p>

      <div className="add-employee-form">
        <div className="form-grid">
          <div className="form-group">
            <label>Employee Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Phone</label>
            <input
              type="text"
              name="phone"
              value={formData.phone || ""}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Designation</label>
            <input
              type="text"
              name="designation"
              value={formData.designation}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Salary</label>
            <input
              type="number"
              name="salary"
              value={formData.salary}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Department</label>

            <select
              name="department_id"
              value={formData.department_id}
              onChange={handleChange}
            >
              <option value="">Select Department</option>

              {departments.map((department) => (
                <option key={department.id} value={department.id}>
                  {department.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EditEmployee;
