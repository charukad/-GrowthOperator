import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { LoginPage } from './features/auth/LoginPage';
import { SignupPage } from './features/auth/SignupPage';
import { WorkspaceListPage } from './features/workspaces/WorkspaceListPage';
import { DashboardLayout } from './features/dashboard/DashboardLayout';
import { TrendDiscovery } from './features/trends/TrendDiscovery';
import { IdeaWorkspace } from './features/ideas/IdeaWorkspace';
import { useAuthStore } from './store/useAuthStore';

const queryClient = new QueryClient();

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route
            path="/workspaces"
            element={
              <ProtectedRoute>
                <WorkspaceListPage />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<Navigate to="/workspaces" />} />
          
          {/* Dashboard Routes */}
          <Route
            path="/dashboard/:workspaceId"
            element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<div className="p-8">Dashboard Home (TBD)</div>} />
            <Route path="trends" element={<TrendDiscovery />} />
            <Route path="ideas" element={<IdeaWorkspace />} />
            <Route path="content" element={<div className="p-8">Content Studio (TBD)</div>} />
            <Route path="analytics" element={<div className="p-8">Analytics (TBD)</div>} />
            <Route path="settings" element={<div className="p-8">Settings (TBD)</div>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
