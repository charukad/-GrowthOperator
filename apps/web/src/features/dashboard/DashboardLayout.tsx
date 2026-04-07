import React from 'react';
import { Outlet, Link, useParams, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/useAuthStore';
import { Layout, TrendingUp, Lightbulb, PenTool, BarChart3, LogOut, Settings } from 'lucide-react';

export const DashboardLayout: React.FC = () => {
  const { workspaceId } = useParams<{ workspaceId: string }>();
  const location = useLocation();
  const clearAuth = useAuthStore((state) => state.clearAuth);

  const navigation = [
    { name: 'Dashboard', href: `/dashboard/${workspaceId}`, icon: Layout },
    { name: 'Trends', href: `/dashboard/${workspaceId}/trends`, icon: TrendingUp },
    { name: 'Ideas', href: `/dashboard/${workspaceId}/ideas`, icon: Lightbulb },
    { name: 'Content', href: `/dashboard/${workspaceId}/content`, icon: PenTool },
    { name: 'Analytics', href: `/dashboard/${workspaceId}/analytics`, icon: BarChart3 },
    { name: 'Settings', href: `/dashboard/${workspaceId}/settings`, icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-sm flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-gray-200">
          <span className="text-xl font-bold text-indigo-600">GrowthOS</span>
        </div>
        
        <nav className="flex-1 px-4 py-4 space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                  isActive
                    ? 'bg-indigo-50 text-indigo-700'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <item.icon
                  className={`mr-3 flex-shrink-0 h-5 w-5 ${
                    isActive ? 'text-indigo-500' : 'text-gray-400'
                  }`}
                />
                {item.name}
              </Link>
            );
          })}
        </nav>
        
        <div className="p-4 border-t border-gray-200">
          <button
            onClick={() => {
              clearAuth();
              window.location.href = '/login';
            }}
            className="flex items-center w-full px-2 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-gray-50 hover:text-gray-900"
          >
            <LogOut className="mr-3 flex-shrink-0 h-5 w-5 text-gray-400" />
            Sign out
          </button>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <main className="flex-1 overflow-y-auto bg-gray-100">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
