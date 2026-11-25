import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function AddEmployee() {
  const navigate = useNavigate();

  // Employee form data
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    designation: "",
    salary: "",
    department_id: "",
  });

  // Department list
  const [departments, setDepartments] = useState([]);

  // Loading and error states
  const [loading, setLoading] = useState(false);
  const [departmentLoading, setDepartmentLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch departments from API
  useEffect(() => {
    async function getDepartments() {
      try {
        const response = await api.get("/departments");
        setDepartments(response.data);
      } catch (error) {
        console.error("Error fetching departments:", error);
        setError("Unable to load departments");
      } finally {
        setDepartmentLoading(false);
      }
    }

    getDepartments();
  }, []);

  // Handle input changes
  function handleChange(e) {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }

  // Handle form submission
  async function handleSubmit(e) {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      const payload = {
        ...formData,
        salary: Number(formData.salary),
        department_id: Number(formData.department_id),
      };

      await api.post("/employees", payload);

      navigate("/employees");
    } catch (error) {
      console.error("Error adding employee:", error);

      setError(error.response?.data?.detail || "Unable to add employee");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="dashboard-content">
      {/* Page Header */}
      <div className="employee-page-header">
        <div>
          <h1>Add New Employee</h1>
          <p>Enter employee information below.</p>
        </div>
      </div>

      {/* Employee Form */}
      <form className="add-employee-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          {/* Employee Name */}
          <div className="form-group">
            <label>Employee Name</label>
            <input
              type="text"
              name="name"
              placeholder="Enter employee name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>

          {/* Email */}
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              placeholder="Enter email address"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          {/* Phone */}
          <div className="form-group">
            <label>Phone</label>
            <input
              type="text"
              name="phone"
              placeholder="Enter phone number"
              value={formData.phone}
              onChange={handleChange}
            />
          </div>

          {/* Designation */}
          <div className="form-group">
            <label>Designation</label>
            <input
              type="text"
              name="designation"
              placeholder="Enter designation"
              value={formData.designation}
              onChange={handleChange}
              required
            />
          </div>

          {/* Salary */}
          <div className="form-group">
            <label>Salary</label>
            <input
              type="number"
              name="salary"
              placeholder="Enter salary"
              value={formData.salary}
              onChange={handleChange}
              min="0"
              step="0.01"
              required
            />
          </div>

          {/* Department Dropdown */}
          <div className="form-group">
            <label>Department</label>

            <select
              name="department_id"
              value={formData.department_id}
              onChange={handleChange}
              required
              disabled={departmentLoading}
            >
              <option value="">
                {departmentLoading
                  ? "Loading departments..."
                  : "Select Department"}
              </option>

              {departments.map((department) => (
                <option key={department.id} value={department.id}>
                  {department.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Error Message */}
        {error && <p className="form-error">{error}</p>}

        {/* Form Buttons */}
        <div className="form-actions">
          <button
            type="submit"
            className="save-employee-btn"
            disabled={loading || departmentLoading}
          >
            {loading ? "Saving..." : "Save Employee"}
          </button>

          <button
            type="button"
            className="cancel-employee-btn"
            onClick={() => navigate("/employees")}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default AddEmployee;
