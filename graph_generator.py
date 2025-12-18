import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json

class GraphValidator:
    '''Validates data for different graph types'''
    
    @staticmethod
    def is_numeric(series):
        return pd.api.types.is_numeric_dtype(series)
    
    @staticmethod
    def is_datetime(series):
        return pd.api.types.is_datetime64_any_dtype(series)
    
    @staticmethod
    def validate(df, graph_type, x_col, y_col, group_col=None):
        '''Validate data based on graph type'''
        errors = []
        warnings = []
        
        if graph_type == 'line':
            if not GraphValidator.is_numeric(df[y_col]):
                errors.append(f"Y-axis '{y_col}' must be numeric for line charts")
            if len(df) < 3:
                errors.append(f"Line chart needs at least 3 data points")
                
        elif graph_type == 'bar':
            if not GraphValidator.is_numeric(df[y_col]):
                errors.append(f"Y-axis '{y_col}' must be numeric")
            if df[x_col].nunique() > 50:
                warnings.append(f"Too many categories ({df[x_col].nunique()}). Consider filtering.")
                
        elif graph_type == 'scatter':
            if not GraphValidator.is_numeric(df[x_col]):
                errors.append(f"X-axis '{x_col}' must be numeric for scatter plots")
            if not GraphValidator.is_numeric(df[y_col]):
                errors.append(f"Y-axis '{y_col}' must be numeric for scatter plots")
            if len(df) < 5:
                warnings.append("Scatter plots work best with at least 5 points")
                
        elif graph_type == 'pie':
            if not GraphValidator.is_numeric(df[y_col]):
                errors.append(f"Values column '{y_col}' must be numeric")
            if df[x_col].nunique() > 8:
                warnings.append(f"Too many categories ({df[x_col].nunique()}). Pie charts work best with ≤8.")
            if df[x_col].nunique() < 2:
                errors.append("Pie chart needs at least 2 categories")
                
        elif graph_type == 'histogram':
            if not GraphValidator.is_numeric(df[x_col]):
                errors.append(f"Column '{x_col}' must be numeric for histogram")
            if len(df) < 10:
                warnings.append("Histograms work best with at least 10 data points")
                
        elif graph_type == 'box':
            if not GraphValidator.is_numeric(df[y_col]):
                errors.append(f"Column '{y_col}' must be numeric for box plot")
                
        elif graph_type == 'candlestick':
            required = ['Date', 'Open', 'High', 'Low', 'Close']
            missing = [col for col in required if col not in df.columns]
            if missing:
                errors.append(f"Missing required columns: {', '.join(missing)}")
                
        elif graph_type == 'heatmap':
            if not GraphValidator.is_numeric(df[y_col]):
                errors.append(f"Value column must be numeric")
                
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }


class GraphGenerator:
    '''Generate Plotly graphs based on validated inputs'''
    
    def __init__(self, df):
        self.df = df
        self.validator = GraphValidator()
    
    def generate(self, graph_type, title, x_col, y_col, group_col=None):
        '''Main generation method'''
        
        # Validate
        validation = self.validator.validate(self.df, graph_type, x_col, y_col, group_col)
        
        if not validation['valid']:
            return {
                'success': False,
                'errors': validation['errors'],
                'warnings': validation['warnings']
            }
        
        # Generate appropriate graph
        try:
            if graph_type == 'line':
                fig = self._line_chart(title, x_col, y_col)
            elif graph_type == 'bar':
                fig = self._bar_chart(title, x_col, y_col)
            elif graph_type == 'scatter':
                fig = self._scatter_plot(title, x_col, y_col, group_col)
            elif graph_type == 'pie':
                fig = self._pie_chart(title, x_col, y_col)
            elif graph_type == 'histogram':
                fig = self._histogram(title, x_col)
            elif graph_type == 'box':
                fig = self._box_plot(title, y_col, group_col)
            elif graph_type == 'candlestick':
                fig = self._candlestick(title)
            elif graph_type == 'heatmap':
                fig = self._heatmap(title, x_col, group_col, y_col)
            elif graph_type == 'area':
                fig = self._area_chart(title, x_col, y_col)
            else:
                return {
                    'success': False,
                    'errors': [f"Graph type '{graph_type}' not supported"]
                }
            
            # FIXED: Use include_plotlyjs=False since we're loading it in the page
            # This prevents double-loading and script conflicts
            html = fig.to_html(
                full_html=False, 
                include_plotlyjs=False,  # Changed from 'cdn' to False
                div_id='plotly-graph'
            )
            
            print(f"Generated HTML length: {len(html)} characters")  # Debug log
            
            return {
                'success': True,
                'html': html,
                'warnings': validation['warnings']
            }
            
        except Exception as e:
            print(f"Error in graph generation: {str(e)}")  # Debug log
            return {
                'success': False,
                'errors': [f"Error generating graph: {str(e)}"]
            }
    
    def _line_chart(self, title, x_col, y_col):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df[x_col],
            y=self.df[y_col],
            mode='lines+markers',
            name=y_col,
            line=dict(width=2, color='#3b82f6'),
            marker=dict(size=4)
        ))
        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            template='plotly_white',
            hovermode='x unified',
            height=500
        )
        return fig
    
    def _bar_chart(self, title, x_col, y_col):
        df_agg = self.df.groupby(x_col)[y_col].sum().reset_index()
        df_agg = df_agg.sort_values(y_col, ascending=False).head(20)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_agg[x_col],
            y=df_agg[y_col],
            marker=dict(color='#3b82f6'),
            text=df_agg[y_col].round(2),
            textposition='auto'
        ))
        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            template='plotly_white',
            height=500
        )
        return fig
    
    def _scatter_plot(self, title, x_col, y_col, color_col=None):
        fig = px.scatter(
            self.df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title,
            template='plotly_white',
            height=500
        )
        return fig
    
    def _pie_chart(self, title, labels_col, values_col):
        df_agg = self.df.groupby(labels_col)[values_col].sum().reset_index()
        df_agg = df_agg.sort_values(values_col, ascending=False).head(8)
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=df_agg[labels_col],
            values=df_agg[values_col],
            hole=0.3,
            textposition='inside',
            textinfo='percent+label'
        ))
        fig.update_layout(
            title=title,
            template='plotly_white',
            height=500
        )
        return fig
    
    def _histogram(self, title, col):
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=self.df[col],
            nbinsx=30,
            marker=dict(color='#3b82f6')
        ))
        fig.update_layout(
            title=title,
            xaxis_title=col,
            yaxis_title='Frequency',
            template='plotly_white',
            height=500
        )
        return fig
    
    def _box_plot(self, title, col, group_col=None):
        if group_col:
            fig = px.box(self.df, x=group_col, y=col, title=title, template='plotly_white')
        else:
            fig = go.Figure()
            fig.add_trace(go.Box(y=self.df[col], name=col))
            fig.update_layout(title=title, template='plotly_white')
        
        fig.update_layout(height=500)
        return fig
    
    def _candlestick(self, title):
        df_recent = self.df.tail(100)
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df_recent['Date'],
            open=df_recent['Open'],
            high=df_recent['High'],
            low=df_recent['Low'],
            close=df_recent['Close']
        ))
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Price',
            template='plotly_white',
            xaxis_rangeslider_visible=False,
            height=500
        )
        return fig
    
    def _heatmap(self, title, x_col, y_col, value_col):
        pivot_df = self.df.pivot_table(
            values=value_col,
            index=y_col,
            columns=x_col,
            aggfunc='mean'
        )
        
        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale='RdYlBu_r'
        ))
        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            template='plotly_white',
            height=500
        )
        return fig
    
    def _area_chart(self, title, x_col, y_col):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df[x_col],
            y=self.df[y_col],
            fill='tozeroy',
            mode='lines',
            line=dict(width=2, color='#3b82f6'),
            fillcolor='rgba(59, 130, 246, 0.3)'
        ))
        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            template='plotly_white',
            height=500
        )
        return fig