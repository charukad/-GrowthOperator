import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams } from 'react-router-dom';
import api from '../../services/api';
import { Search, Loader2, Sparkles, ExternalLink, Activity } from 'lucide-react';

export const TrendDiscovery: React.FC = () => {
  const { workspaceId } = useParams<{ workspaceId: string }>();
  const [niche, setNiche] = useState('');
  const [scraping, setScraping] = useState(false);
  const queryClient = useQueryClient();

  const { data: trends, isLoading } = useQuery({
    queryKey: ['trends', workspaceId],
    queryFn: async () => {
      const response = await api.get(`/trends/?workspace_id=${workspaceId}`);
      return response.data;
    },
    enabled: !!workspaceId,
  });

  const scrapeMutation = useMutation({
    mutationFn: async (targetNiche: string) => {
      const response = await api.post('/trends/scrape', {
        workspace_id: workspaceId,
        niche: targetNiche,
      });
      return response.data;
    },
    onSuccess: () => {
      setScraping(true);
      // Simulating polling or waiting for celery task
      setTimeout(() => {
        setScraping(false);
        queryClient.invalidateQueries({ queryKey: ['trends', workspaceId] });
      }, 5000);
    },
  });

  const generateIdeasMutation = useMutation({
    mutationFn: async (trendId: string) => {
      const response = await api.post('/ideas/generate', {
        workspace_id: workspaceId,
        trend_id: trendId,
        count: 3,
      });
      return response.data;
    },
    onSuccess: () => {
      alert("Ideas generated successfully! Check the Ideas tab.");
    },
  });

  const handleScrape = (e: React.FormEvent) => {
    e.preventDefault();
    if (niche.trim()) {
      scrapeMutation.mutate(niche.trim());
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Trend Discovery</h1>
          <p className="text-gray-500 text-sm mt-1">Discover viral content opportunities in your niche.</p>
        </div>
      </div>

      {/* Scrape Header */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-8">
        <form onSubmit={handleScrape} className="flex gap-4">
          <div className="flex-1 relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Enter a niche or subreddit (e.g., 'SaaS', 'marketing')"
              value={niche}
              onChange={(e) => setNiche(e.target.value)}
            />
          </div>
          <button
            type="submit"
            disabled={scraping || scrapeMutation.isPending}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
          >
            {(scraping || scrapeMutation.isPending) ? (
              <><Loader2 className="animate-spin -ml-1 mr-2 h-4 w-4" /> Analyzing...</>
            ) : (
              'Scan Trends'
            )}
          </button>
        </form>
      </div>

      {/* Trend Cards */}
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <Loader2 className="animate-spin h-8 w-8 text-indigo-500" />
        </div>
      ) : trends?.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg border border-dashed border-gray-300">
          <Activity className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No trends found</h3>
          <p className="mt-1 text-sm text-gray-500">Scan a niche to discover emerging trends.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {trends?.map((trend: any) => (
            <div key={trend.id} className="bg-white overflow-hidden shadow-sm rounded-lg border border-gray-200 hover:border-indigo-300 transition-colors flex flex-col">
              <div className="p-5 flex-1">
                <div className="flex items-center justify-between mb-3">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {trend.source}
                  </span>
                  <span className="text-xs text-gray-500 flex items-center">
                    <Activity className="w-3 h-3 mr-1" />
                    Score: {trend.virality_score || 0}
                  </span>
                </div>
                <a href={trend.url} target="_blank" rel="noopener noreferrer" className="block mt-2">
                  <p className="text-lg font-semibold text-gray-900 hover:text-indigo-600 transition-colors line-clamp-2">
                    {trend.title} <ExternalLink className="inline-block w-4 h-4 ml-1 opacity-50" />
                  </p>
                </a>
                <p className="mt-3 text-sm text-gray-500 line-clamp-3">
                  {trend.summary || 'No summary available.'}
                </p>
              </div>
              <div className="bg-gray-50 px-5 py-3 border-t border-gray-200">
                <button
                  onClick={() => generateIdeasMutation.mutate(trend.id)}
                  disabled={generateIdeasMutation.isPending && generateIdeasMutation.variables === trend.id}
                  className="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 disabled:opacity-50"
                >
                  {generateIdeasMutation.isPending && generateIdeasMutation.variables === trend.id ? (
                    <Loader2 className="animate-spin -ml-1 mr-2 h-4 w-4" />
                  ) : (
                    <Sparkles className="w-4 h-4 mr-2" />
                  )}
                  Auto-Generate Ideas
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
