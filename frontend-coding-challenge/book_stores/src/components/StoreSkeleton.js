import './StoreSkeleton.css';

const StoreSkeleton = () => (
    <div class="store-skeleton-container">
        <div class="store-skeleton-image" />
        <div class="store-skeleton-body">
            <div class="store-skeleton-line" />
            <div style={{ marginTop: '0.75rem' }}>
                <div class="grid grid-cols-3 gap-4">
                    <div class="store-skeleton-line" />
                    <div class="store-skeleton-line" />
                </div>
                <div class="store-skeleton-line" />
                <div class="store-skeleton-line" />
            </div>
        </div>
    </div>
);

export default StoreSkeleton;