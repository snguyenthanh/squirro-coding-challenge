import { useQuery } from 'react-query';
import { getStores } from '../loaders/stores';
import { getPopularBooksForStores } from '../loaders/books';

import Store from './Store';
import StoreSkeleton from './StoreSkeleton';
import './StoreList.css';

const StoreList = () => {
    const { isLoading: isStoresLoading, data: stores, error } = useQuery(
        'getStores',
        getStores,
        {
            retry: 1,
        },
    );
    const { data: popularBooksForStores } = useQuery(
        'getPopularBooksForStores',
        async () => await getPopularBooksForStores(stores),
        {
            retry: 1,
            enabled: !!stores && stores.length > 0,
        },
    );
    
    if (error) throw error;

    return (
        <div className="store-list">
            {isStoresLoading && <StoreSkeleton />}
            {stores && stores.map((store, storeIdx) => (
                <Store
                    key={`store-listitem-${store.id}`}
                    store={store.attributes}
                    storeCountryCode={store?.relationships?.countries?.data?.attributes?.code}
                    popularBooks={popularBooksForStores && popularBooksForStores[storeIdx]}
                />
            ))}
        </div>
    )
};

export default StoreList;