#!/usr/bin/env python3
"""
Knowledge Graph Visualization Script

This script connects to the database and visualizes the policy cross-links
as a knowledge graph using various layout algorithms.
"""

import argparse
import sys
import os
from collections import defaultdict
import json

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import networkx as nx  # type: ignore
    import matplotlib.pyplot as plt  # type: ignore
    import matplotlib.cm as cm  # type: ignore
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False
    nx = None  # type: ignore
    plt = None  # type: ignore
    cm = None  # type: ignore
    print("Warning: NetworkX and/or matplotlib not installed. Install with: pip install networkx matplotlib")

try:
    import plotly.graph_objects as go  # type: ignore
    import plotly.express as px  # type: ignore
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    go = None  # type: ignore
    px = None  # type: ignore
    print("Warning: Plotly not installed. Install with: pip install plotly")

def get_database_connection():
    """Get database connection using existing utilities"""
    try:
        from ingest_pipeline.utils import get_session
        from ingest_pipeline.models import Policy, PolicyCrossLink
        print("Database modules imported successfully")
        return get_session, Policy, PolicyCrossLink
    except Exception as e:
        print(f"Failed to import database modules: {e}")
        raise

def fetch_knowledge_graph_data(lpa_code=None):
    """Fetch policy and cross-link data from the database"""
    get_session, Policy, PolicyCrossLink = get_database_connection()
    
    try:
        with get_session() as session:
            print("Database session created successfully")
            
            # Fetch policies
            if lpa_code:
                policy_query = session.query(Policy).filter(Policy.lpa_code == lpa_code)
                print(f"Querying policies for LPA: {lpa_code}")
            else:
                policy_query = session.query(Policy)
                print("Querying all policies")
            
            policies = {}
            policy_list = policy_query.all()
            print(f"Found {len(policy_list)} policies")
            
            for policy in policy_list:
                policies[policy.policy_id] = {
                    'title': policy.policy_title or policy.policy_id,
                    'summary': policy.summary or ''
                }
            
            # Fetch cross-links
            if lpa_code:
                # Get cross-links where source policy belongs to the LPA
                links_query = (
                    session.query(PolicyCrossLink)
                    .join(Policy, PolicyCrossLink.source_policy_code == Policy.policy_id)
                    .filter(Policy.lpa_code == lpa_code)
                )
                print(f"Querying cross-links for LPA: {lpa_code}")
            else:
                links_query = session.query(PolicyCrossLink)
                print("Querying all cross-links")
            
            cross_links = []
            links_list = links_query.all()
            print(f"Found {len(links_list)} cross-links")
            
            for link in links_list:
                cross_links.append((link.source_policy_code, link.target_policy_code))
            
            return policies, cross_links
            
    except Exception as e:
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc()
        raise

def analyze_graph_structure(policies, cross_links):
    """Analyze the structure of the knowledge graph"""
    # Build adjacency lists
    outgoing = defaultdict(list)
    incoming = defaultdict(list)
    all_nodes = set(policies.keys())
    
    for source, target in cross_links:
        outgoing[source].append(target)
        incoming[target].append(source)
        all_nodes.add(source)
        all_nodes.add(target)
    
    # Calculate metrics
    stats = {
        'total_policies': len(policies),
        'total_nodes': len(all_nodes),
        'total_edges': len(cross_links),
        'connected_components': 0,
        'orphaned_nodes': 0,
        'most_connected': [],
        'hub_nodes': [],
        'authority_nodes': []
    }
    
    # Find most connected nodes
    connection_counts = defaultdict(int)
    for source, target in cross_links:
        connection_counts[source] += 1
        connection_counts[target] += 1
    
    stats['most_connected'] = sorted(
        connection_counts.items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:10]
    
    # Find hub nodes (many outgoing) and authority nodes (many incoming)
    stats['hub_nodes'] = sorted(
        [(node, len(links)) for node, links in outgoing.items()], 
        key=lambda x: x[1], 
        reverse=True
    )[:5]
    
    stats['authority_nodes'] = sorted(
        [(node, len(links)) for node, links in incoming.items()], 
        key=lambda x: x[1], 
        reverse=True
    )[:5]
    
    # Count orphaned nodes
    connected_nodes = set()
    for source, target in cross_links:
        connected_nodes.add(source)
        connected_nodes.add(target)
    
    stats['orphaned_nodes'] = len(all_nodes - connected_nodes)
    
    return stats

def create_networkx_graph(policies, cross_links):
    """Create a NetworkX graph from the policy data"""
    if not HAS_NETWORKX:
        raise ImportError("NetworkX not available")
    
    G = nx.DiGraph()
    
    # Add nodes with attributes
    for policy_id, policy_data in policies.items():
        G.add_node(policy_id, 
                  title=policy_data['title'],
                  summary=policy_data['summary'][:100] + '...' if len(policy_data['summary']) > 100 else policy_data['summary'])
    
    # Add edges
    for source, target in cross_links:
        G.add_edge(source, target)
    
    return G

def visualize_with_matplotlib(policies, cross_links, output_file=None, layout='spring'):
    """Create a matplotlib visualization of the knowledge graph"""
    if not HAS_NETWORKX:
        print("NetworkX not available, skipping matplotlib visualization")
        return
    
    G = create_networkx_graph(policies, cross_links)
    
    plt.figure(figsize=(20, 16))
    
    # Choose layout
    if layout == 'spring':
        pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G)
    elif layout == 'hierarchical':
        # Try to create a hierarchical layout
        try:
            pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
        except:
            pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    else:
        pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Calculate node sizes based on degree
    node_sizes = []
    for node in G.nodes():
        degree = G.degree(node)
        size = max(300, degree * 100)  # Minimum size 300, scale by degree
        node_sizes.append(size)
    
    # Calculate node colors based on in-degree (authority)
    in_degrees = [G.in_degree(node) for node in G.nodes()]
    max_in_degree = max(in_degrees) if in_degrees else 1
    node_colors = [degree / max_in_degree for degree in in_degrees]
    
    # Draw the graph
    nx.draw_networkx_nodes(G, pos, 
                          node_size=node_sizes,
                          node_color=node_colors,
                          cmap=plt.cm.YlOrRd,
                          alpha=0.7)
    
    nx.draw_networkx_edges(G, pos, 
                          edge_color='gray',
                          arrows=True,
                          arrowsize=20,
                          arrowstyle='->',
                          alpha=0.5,
                          width=0.5)
    
    # Add labels for important nodes
    important_nodes = [node for node in G.nodes() if G.degree(node) >= 3]
    important_labels = {node: node for node in important_nodes}
    
    nx.draw_networkx_labels(G, pos, 
                           labels=important_labels,
                           font_size=8,
                           font_weight='bold')
    
    plt.title(f"Policy Knowledge Graph\n{len(G.nodes())} nodes, {len(G.edges())} edges", 
              fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Graph saved to {output_file}")
    else:
        plt.show()

def visualize_with_plotly(policies, cross_links, output_file=None):
    """Create an interactive Plotly visualization"""
    if not HAS_PLOTLY:
        print("Plotly not available, skipping interactive visualization")
        return
    
    if not HAS_NETWORKX:
        print("NetworkX not available, skipping Plotly visualization")
        return
    
    G = create_networkx_graph(policies, cross_links)
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Prepare edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(x=edge_x, y=edge_y,
                           line=dict(width=0.5, color='#888'),
                           hoverinfo='none',
                           mode='lines')
    
    # Prepare node traces
    node_x = []
    node_y = []
    node_text = []
    node_size = []
    node_color = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Node info
        policy_data = policies.get(node, {'title': node, 'summary': ''})
        degree = G.degree(node)
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)
        
        node_text.append(f"Policy: {node}<br>" +
                        f"Title: {policy_data['title']}<br>" +
                        f"Connections: {degree} (in: {in_degree}, out: {out_degree})<br>" +
                        f"Summary: {policy_data['summary'][:100]}...")
        
        node_size.append(max(10, degree * 5))
        node_color.append(in_degree)
    
    node_trace = go.Scatter(x=node_x, y=node_y,
                           mode='markers+text',
                           text=[node for node in G.nodes()],
                           textposition="middle center",
                           textfont=dict(size=8),
                           hovertext=node_text,
                           hoverinfo='text',
                           marker=dict(size=node_size,
                                     color=node_color,
                                     colorscale='YlOrRd',
                                     colorbar=dict(title="In-Degree"),
                                     line=dict(width=2, color='black')))
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title=dict(
                           text=f'Interactive Policy Knowledge Graph<br>{len(G.nodes())} policies, {len(G.edges())} cross-references',
                           font=dict(size=16)
                       ),
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20,l=5,r=5,t=40),
                       annotations=[ dict(
                           text="Hover over nodes for details. Node size = total connections, color = incoming references",
                           showarrow=False,
                           xref="paper", yref="paper",
                           x=0.005, y=-0.002,
                           xanchor="left", yanchor="bottom",
                           font=dict(color="#666666", size=12)
                       )],
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    
    if output_file:
        fig.write_html(output_file)
        print(f"Interactive graph saved to {output_file}")
    else:
        fig.show()

def print_statistics(stats):
    """Print knowledge graph statistics"""
    print("\n" + "="*60)
    print("KNOWLEDGE GRAPH STATISTICS")
    print("="*60)
    print(f"Total policies in DB: {stats['total_policies']}")
    print(f"Total nodes in graph: {stats['total_nodes']}")
    print(f"Total edges (cross-links): {stats['total_edges']}")
    print(f"Orphaned nodes: {stats['orphaned_nodes']}")
    
    if stats['most_connected']:
        print(f"\nMost Connected Policies:")
        for i, (node, connections) in enumerate(stats['most_connected'][:5], 1):
            print(f"  {i}. {node}: {connections} connections")
    
    if stats['hub_nodes']:
        print(f"\nTop Hub Nodes (most outgoing references):")
        for i, (node, out_degree) in enumerate(stats['hub_nodes'][:5], 1):
            print(f"  {i}. {node}: {out_degree} outgoing")
    
    if stats['authority_nodes']:
        print(f"\nTop Authority Nodes (most incoming references):")
        for i, (node, in_degree) in enumerate(stats['authority_nodes'][:5], 1):
            print(f"  {i}. {node}: {in_degree} incoming")

def export_graph_data(policies, cross_links, output_file):
    """Export graph data to JSON format"""
    graph_data = {
        'nodes': [
            {
                'id': policy_id,
                'title': policy_data['title'],
                'summary': policy_data['summary']
            }
            for policy_id, policy_data in policies.items()
        ],
        'links': [
            {
                'source': source,
                'target': target
            }
            for source, target in cross_links
        ]
    }
    
    with open(output_file, 'w') as f:
        json.dump(graph_data, f, indent=2)
    
    print(f"Graph data exported to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Visualize policy knowledge graph")
    parser.add_argument("--lpa", help="Filter by LPA code")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--format", choices=['matplotlib', 'plotly', 'json', 'stats'], 
                       default='stats', help="Output format")
    parser.add_argument("--layout", choices=['spring', 'circular', 'kamada_kawai', 'hierarchical'],
                       default='spring', help="Layout algorithm for matplotlib")
    
    args = parser.parse_args()
    
    print("Fetching knowledge graph data...")
    policies, cross_links = fetch_knowledge_graph_data(args.lpa)
    
    if not policies and not cross_links:
        print("No data found. Make sure the database contains policy data.")
        return
    
    print(f"Loaded {len(policies)} policies and {len(cross_links)} cross-links")
    
    # Analyze graph structure
    stats = analyze_graph_structure(policies, cross_links)
    
    if args.format == 'stats':
        print_statistics(stats)
    
    elif args.format == 'matplotlib':
        visualize_with_matplotlib(policies, cross_links, args.output, args.layout)
    
    elif args.format == 'plotly':
        visualize_with_plotly(policies, cross_links, args.output)
    
    elif args.format == 'json':
        if not args.output:
            args.output = 'knowledge_graph.json'
        export_graph_data(policies, cross_links, args.output)
    
    print("\nVisualization complete!")

if __name__ == "__main__":
    main()
