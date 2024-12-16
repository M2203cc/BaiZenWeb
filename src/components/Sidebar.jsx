import React, { useState } from 'react';
import { FaShoppingBag, FaLayerGroup, FaVideo, FaStore, FaBox, FaList } from 'react-icons/fa';
import '../styles/Sidebar.css';

const Sidebar = () => {
  const [isDiscoverOpen, setIsDiscoverOpen] = useState(false);

  const toggleDiscover = () => {
    setIsDiscoverOpen(!isDiscoverOpen);
  };

  return (
    <div className="sidebar">
      <div className="sidebar-section">
        <h3>SOCIAL LISTENING & AI</h3>
        <div className="sidebar-item">
          <FaShoppingBag />
          <span>My Brand</span>
        </div>
        
        {/* Discover 下拉菜单 */}
        <div className="sidebar-dropdown">
          <div className="sidebar-item" onClick={toggleDiscover}>
            <FaLayerGroup />
            <span>Discover</span>
            <span className={`arrow ${isDiscoverOpen ? 'open' : ''}`}>▼</span>
          </div>
          
          {isDiscoverOpen && (
            <div className="sidebar-submenu">
              <div className="sidebar-item">
                <FaVideo />
                <span>Videos</span>
              </div>
              <div className="sidebar-item">
                <FaStore />
                <span>Brands</span>
              </div>
              <div className="sidebar-item">
                <FaBox />
                <span>Products</span>
              </div>
              <div className="sidebar-item">
                <FaList />
                <span>Categories</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Sidebar; 