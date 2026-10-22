import {createContext, useContext} from 'react';

// false = "clean" master without on-screen copy, for adding captions/logo in the edit.
export const CaptionsOn = createContext(true);
export const useCaptions = () => useContext(CaptionsOn);
