import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { LoginPage } from './features/auth/LoginPage';
import { SignupPage } from './features/auth/SignupPage';
import { WorkspaceListPage } from './features/workspaces/WorkspaceListPage';
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
          <Route
            path="/dashboard/:workspaceId"
            element={
              <ProtectedRoute>
                <div className="p-8">Dashboard for workspace (TBD)</div>
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
