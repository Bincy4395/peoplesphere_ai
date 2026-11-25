import DepartmentStats from "../components/DepartmentStats";
import RecentEmployees from "../components/RecentEmployees";
import ProjectProgress from "../components/ProjectProgress";
import QuickActions from "../components/QuickActions";
import ChatbotWidget from "../components/ChatbotWidget";

function Dashboard() {
  return (
    <div className="dashboard-content">
      <h1>Dashboard</h1>

      <p>Welcome back! Here's your workforce overview.</p>

      <div className="dashboard-cards">
        <div className="dashboard-card">
          <h3>Total Employees</h3>
          <h2>120</h2>
        </div>

        <div className="dashboard-card">
          <h3>Departments</h3>
          <h2>08</h2>
        </div>

        <div className="dashboard-card">
          <h3>Active Projects</h3>
          <h2>15</h2>
        </div>

        <div className="dashboard-card">
          <h3>Leave Requests</h3>
          <h2>06</h2>
        </div>
      </div>

      <DepartmentStats />

      <RecentEmployees />

      <ProjectProgress />

      <QuickActions />

      <ChatbotWidget />
    </div>
  );
}

export default Dashboard;
