import './BookTable.css';

const BookTable = ({ storeKey, books }) => (
    <table className="book-table">
        <colgroup>
            <col className="w-full" />
            <col />
        </colgroup>
        <thead >
            <tr>
                <th scope="col">
                Book
                </th>
                <th scope="col">
                Author
                </th>
            </tr>
        </thead>
        <tbody>
            {books.map((book) => (
                <tr key={`bookstore-${storeKey}-book-${book.attributes.name}`}>
                    <td>
                        <div>{book.attributes.name}</div>
                    </td>
                    <td>
                        {book?.relationships?.author?.data?.attributes?.fullName || 'N/A'}
                    </td>
                </tr>
            ))}
        </tbody>
    </table>
);

export default BookTable;