import { StarIcon } from '@heroicons/react/20/solid'
import classNames from 'classnames';

import BookTable from './BookTable';
import EmptyState from '../EmptyState';
import './Store.css';

const Store = ({ store, storeCountryCode, popularBooks = null }) => {
    return (
        <div className="store-container">
            <div className="store">
                {/* Store details */}
                <div className="store-details">
                    <h1 className="store-title">{store.name}</h1>

                    <section aria-labelledby="information-heading" style={{ marginTop: '1rem' }}>
                        <h2 id="information-heading" className="screen-reader-only">
                            Store information
                        </h2>

                        <div className="flex-align-center">
                            <div className="store-flag">
                                <span class={`fi fi-${storeCountryCode.toLowerCase()}`} />
                            </div>

                            <div className="store-rating-container">
                                <h2 className="screen-reader-only">Reviews</h2>
                                <div className="store-rating">
                                    {[0, 1, 2, 3, 4].map((rating) => (
                                        <StarIcon
                                        key={rating}
                                        className={classNames(
                                            store.rating > rating ? 'active' : 'inactive',
                                        )}
                                        aria-hidden="true"
                                        />
                                    ))}
                                </div>
                                <p className="screen-reader-only">{store.rating} out of 5 stars</p>
                            </div>
                        </div>
                        
                        <div className="store-establishment-date">
                            <p>{`Since ${store.establishmentDate}`}</p>
                        </div>

                        <p className="store-description">
                            Check out their books at{' '}
                            <a href={store.website} target="_blank" rel="noreferrer">
                                {store.website}
                            </a>
                        </p>

                        <div className="store-description-separator" />

                        <div>
                            <h3 className="store-popular-books-title">
                                Best-selling books
                            </h3>
                            {(popularBooks && popularBooks.length > 0) ? (
                                <BookTable storeKey={store.id} books={popularBooks} />
                            ) : (
                                <EmptyState
                                    title="No popular books"
                                    description="This bookstore doesn't have any books yet."
                                />
                            )}
                        </div>
                    </section>
                </div>

                {/* Store image */}
                <div className="store-image-container">
                    <img
                        src={store.storeImage}
                        alt={`Store ${store.name}`}
                        className="store-image"
                        loading="lazy"
                    />
                </div>
            </div>
        </div>
    );
}

export default Store;