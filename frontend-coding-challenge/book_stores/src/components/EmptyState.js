import './EmptyState.css';

const EmptyState = ({ title, description }) => (
    <div className="empty-state">
        <h2>{title}</h2>
        <p>{description}</p>
    </div>
);

export default EmptyState;