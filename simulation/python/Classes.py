import numpy as np

class PNN:
    """Creates a Photonic Neural Network model using INTERCONNECT        

        Parameters
        ----------
        model : {'parallel', 'series'}
            PNN model.
        taps : int
            number of taps for this PNN (Default is 4).
        DelayUnitLen : float
            length (in meters) of the basic delay unit of the PNN. (Default is 100e-6).
        unitsNextTap : int
            number of units each consecutive tap adds, depending of the model. (Default is 1).
        WvgLoss : float
            waveguide loss value, including PPC Cells waveguides, in dB/m. (Default is 0)
        
        Attributes
        ------- 
        bitrate : float
            system's symbol rate in Symbols/s. (Default is 10e9).
        numofSamples : float
            simulation's number of samples. (Default is 8192).
        timeWindow : float
            simulation's total time in seconds. (Default is 5.12e-9).
        FiberLen : float
            fiber length in meters. (Default is 1000).
        PRBSType : {'PRBS', 'zeros', 'ones', 'alternate', 'codeword', 'load from file'}
            rule of the pseudo-random bit sequence. (Default is PRBS, random).
        PulseAmp : float
            pulse generator amplitude in a.u. (Default is 1).
        RiseTime : float
            pulse generator rise time period ratio (Default is 0.05).
        FallTime : float
            pulse generator fall time period ratio (Default is 0.05).
        MZMILoss : float
            insertion loss on Mark-Zehnder Modulator in dB (Default is 0).
        ToggleBitOp : bool
            Enables or Disables a fork after the PRBS, for logical XOR analysis. (Default is false).
        OutputType : {'connected','disconnected','mixed'}
            PNN output topology: (Default is 'connected')
            - 'connected': all arms connected and combined to a single photodetector.
            - 'disconnected': each arm leads to an individual photodetector.
            - 'mixed': each arm splits leading to both configurations.
            
        ToggleAWGN : bool
            Enables or Disables Additive Gaussian White Noise after the PD. (Default is false).
        NoisePSD : float
            Additive Gaussian White Noise power spectral density after the PD in W/Hz. Needs to be toggled on. (Default is 2e-20)
        ToggleOptFilter : bool
             Enables or Disables an Optical Filter before the receiver photodiode. (Default is false).
        OptFilterBand : float
             Optical Filter band in Hz. Needs to be toggled on. (Default is 25e9)
        PDResponsivity : float
            PD Responsivity in A/W. (Default is 1).
        PDDarkCurrent : float
            PD Dark Current in A. (Default is 0).
        PDTNoise : float
            PD Thermal Noise in A/Hz^.5. Needs to be toggled on. (Default is 1e-22).
        TogglePDTNoise : bool
            Enables or Disables PD Thermal Noise. (Default is false).
        TogglePDSNoise : bool
            Enables or Disables PD Shot Noise. (Default is false).

        Methods
        ------- 
        showParameters()
            used to show an overview of all attributes and its values.
        mount(process)
            used to assembling the model in INTERCONNECT, given the attributes.
        update(process)
            updates an already assembled model in INTERCONNECT, given the attributes.
        setAttributes(**kwargs)
            modify any set of variables in this instance.
        getAttributes(*kwargs)
            return any set of variables in this instance.

        Notes
        ------- 
        In this class, some **methods** are included only for visual and organization purposes.
        Each of them has its own descriptions and are limited to only alter attributes in a 
        certain domain of the model:

            - general
            - transmission
            - simulation
            - output
            - photoreceptor
    """

    # Transmission local parameters
    FiberLen = 1e3
    PRBSType = 'PRBS'
    PulseAmp = 1
    RiseTime = 0.05
    FallTime = 0.05
    MZMILoss = 0
    ToggleBitOp = True

    # Simulation local parameters
    bitrate = 10e9
    numofSamples = 8192
    timeWindow = 5.12e-9

    # Output local parameters
    OutputType = 'connected'
    ToggleAWGN = False
    NoisePSD = 2e-20
    ToggleOptFilter = False
    OptFilterBand = 25e9

    # Photoreceptor local parameters
    PDResponsivity = 1
    PDDarkCurrent = 0
    PDTNoise = 1e-22
    TogglePDTNoise = False
    TogglePDSNoise = False
    

    def __init__(self, model='parallel', taps=4, DelayUnitLen=100e-6, unitsNextTap=1, WvgLoss=0):
        if model not in [None,'parallel','series']: raise NameError(f'model: No model type named {model}. Use parallel or series.')
        else: self.model = model
        self.taps = taps
        self.DelayUnitLen = DelayUnitLen
        self.unitsNextTap = unitsNextTap
        self.WvgLoss = WvgLoss


    def general(self,model=None, taps=None, DelayUnitLen=None, unitsNextTap=None, WvgLoss=None):
        """Method specialized for altering any general attribute of the PNN model.       

        Parameters
        ----------
        model : {'parallel', 'series'}
            PNN model.
        taps : int
            number of taps for this PNN (Default is 4).
        DelayUnitLen : float
            length (in meters) of the basic delay unit of the PNN. (Default is 100e-6).
        unitsNextTap : int
            number of units each consecutive tap adds, depending of the model. (Default is 1).
        WvgLoss : float
            waveguide loss value, including PPC Cells waveguides, in dB/m. (Default is 0)
        """
        if model not in [None,'parallel','series']: raise NameError(f'model: No model type named {model}. Use parallel or series.')
        elif model is not None: self.model = model
        if taps is not None: self.taps = taps
        if DelayUnitLen is not None: self.DelayUnitLen = DelayUnitLen
        if unitsNextTap is not None: self.unitsNextTap = unitsNextTap
        if WvgLoss is not None: self.WvgLoss = WvgLoss


    def transmission(self,FiberLen=None,PRBSType=None,PulseAmp=None,RiseTime=None,FallTime=None,MZMILoss=None,ToggleBitOp=None):
        """Method specialized for altering any attribute related to transmission side of the PNN.       

        Parameters
        ----------
        FiberLen : float
            fiber length in meters. (Default is 1000).
        PRBSType : {'PRBS', 'zeros', 'ones', 'alternate', 'codeword', 'load from file'}
            rule of the pseudo-random bit sequence. (Default is PRBS, random).
        PulseAmp : float
            pulse generator amplitude in a.u. (Default is 1).
        RiseTime : float
            pulse generator rise time period ratio (Default is 0.05).
        FallTime : float
            pulse generator fall time period ratio (Default is 0.05).
        MZMILoss : float
            insertion loss on Mark-Zehnder Modulator in dB (Default is 0).
        ToggleBitOp : bool
            Enables or Disables a fork after the PRBS, for logical XOR analysis. (Default is false).
        """
        if FiberLen is not None: self.FiberLen = FiberLen
        if PRBSType is not None: self.PRBSType = PRBSType
        if PulseAmp is not None: self.PulseAmp = PulseAmp
        if RiseTime is not None: self.RiseTime = RiseTime
        if FallTime is not None: self.FallTime = FallTime
        if MZMILoss is not None: self.MZMILoss = MZMILoss
        if ToggleBitOp is not None: self.ToggleBitOp = ToggleBitOp


    def simulation(self,bitrate=None,numofSamples=None,timeWindow=None):
        """Method specialized for altering any attribute related to simulation environment in INTERCONNECT.       

        Parameters
        ----------
        bitrate : float
            system's symbol rate in Bits/s. (Default is 10e9).
        numofSamples : float
            simulation's number of samples. (Default is 8192).
        timeWindow : float
            simulation's total time in seconds. (Default is 5.12e-9).
        """
        if bitrate is not None: self.bitrate = bitrate
        if numofSamples is not None: self.numofSamples = numofSamples
        if timeWindow is not None: self.timeWindow = timeWindow


    def output(self,OutputType=None,ToggleAWGN=None,NoisePSD=None,ToggleOptFilter=None,OptFilterBand=None):
        """Method specialized for altering any attribute related to output topology of the PNN.       

        Parameters
        ----------
        OutputType : {'connected','disconnected','mixed'}
            PNN output topology: (Default is 'connected')
            - 'connected': all arms connected and combined to a single photodetector.
            - 'disconnected': each arm leads to an individual photodetector.
            - 'mixed': each arm splits leading to both configurations.
            
        ToggleAWGN : bool
            Enables or Disables Additive Gaussian White Noise after the PD. (Default is false).
        NoisePSD : float
            Additive Gaussian White Noise power spectral density after the PD in W/Hz. Needs to be toggled on. (Default is 2e-20)
        ToggleOptFilter : bool
             Enables or Disables an Optical Filter before the receiver photodiode. (Default is false).
        OptFilterBand : float
             Optical Filter band in Hz. Needs to be toggled on. (Default is 25e9)
        """
        if OutputType not in [None,'connected','disconnected','mixed']: raise NameError(f'OutputType: No output type named {OutputType}. Use connected, disconnected or mixed.')
        elif OutputType is not None: self.OutputType = OutputType
        if ToggleAWGN is not None: self.ToggleAWGN = ToggleAWGN
        if NoisePSD is not None: self.NoisePSD = NoisePSD
        if ToggleOptFilter is not None: self.ToggleOptFilter = ToggleOptFilter
        if OptFilterBand is not None: self.OptFilterBand = OptFilterBand

    def photoreceptor(self,PDResponsivity=None,PDDarkCurrent=None,PDTNoise=None,TogglePDTNoise=None,TogglePDSNoise=None):
        """Method specialized for altering any attribute related to photoreceptor in PNN's output.       

        Parameters
        ----------
        PDResponsivity : float
            PD Responsivity in A/W. (Default is 1).
        PDDarkCurrent : float
            PD Dark Current in A. (Default is 0).
        PDTNoise : float
            PD Thermal Noise in A/Hz^.5. Needs to be toggled on. (Default is 1e-22).
        TogglePDTNoise : bool
            Enables or Disables PD Thermal Noise. (Default is false).
        TogglePDSNoise : bool
            Enables or Disables PD Shot Noise. (Default is false).
        """
        if PDResponsivity is not None: self.PDResponsivity = PDResponsivity
        if PDDarkCurrent is not None: self.PDDarkCurrent = PDDarkCurrent
        if PDTNoise is not None: self.PDTNoise = PDTNoise
        if TogglePDTNoise is not None: self.TogglePDTNoise = TogglePDTNoise
        if TogglePDSNoise is not None: self.TogglePDSNoise = TogglePDSNoise



    def showParameters(self):
        """Method used to show an overview of all attributes and its values"""
        import numpy as np
        print(f'general :: Model: {self.model} | Taps: {self.taps} | Delay Unit Length: {self.DelayUnitLen*1e-6} μm | Units for next tap: {self.unitsNextTap} | Wvg Loss: {self.WvgLoss} dB/m')
        print(f'transmission :: Fiber length: {self.FiberLen*1e-3} km | PRBS Type: {self.PRBSType} | Pulse Amplitude: {self.PulseAmp} | Rise/Fall Period: {self.RiseTime}/{self.FallTime} | MZM Insetion Loss: {self.MZMILoss} dB')
        print(f'simulation :: Bit Rate: {np.round(1e-9*self.bitrate,2)} Gbits/s | Number of Samples: {self.numofSamples} | Time Window: {self.timeWindow} s')
        print(f'photoreceptor :: PD Responsivity: {self.PDResponsivity} A/W | PD Dark Current: {self.PDDarkCurrent} A | PD Thermal Noise: {self.PDTNoise} A/Hz^.5')
        print(f'output :: AWGN PSD: {self.NoisePSD} W/Hz | Optical Filter bandwidth: {self.OptFilterBand*1e-9} GHz')
        print(f'-----------------------------------------------------------------------------------')
        print(f'XOR Operator: {"enabled" if self.ToggleBitOp == True else "disabled"}')
        print(f'PD Thermal Noise: {"enabled" if self.TogglePDTNoise == True else "disabled"}')
        print(f'PD Shot Noise: {"enabled" if self.TogglePDSNoise == True else "disabled"}')
        print(f'AWGN post PD: {"enabled" if self.ToggleAWGN == True else "disabled"}')
        print(f'Optical Filter: {"enabled" if self.ToggleOptFilter == True else "disabled"}')
        print(f'Output Type: {self.OutputType}')

    # Set and Get attributes -------------------------------------------

    def setAttributes(self, **kwargs):
        """Modify any set of variables in this instance

        Parameters
        ----------
        **kwargs 
            set of local variables to modify 

        Returns
        -------
        none
        
        """
        for key, value in kwargs.items():
            setattr(self,key,value)

    

    def getAttributes(self, *kwargs):
        """Return any set of variables in this instance

        Parameters
        ----------
        *kwargs : str 
            set of local variables names

        Returns
        -------
        tuple
            returns a tuple of values from each parameter requested
        
        """
        return tuple(getattr(self, attr, None) for attr in kwargs)
    

    # Parameter update section -----------------------------------------

    def update(self,process):    
        """Method used to update an already assembled model in INTERCONNECT, given the attributes."""    
        process.switchtolayout()

        process.setnamed('::Root Element','bitrate',self.bitrate)
        process.setnamed('::Root Element','time window',self.timeWindow)
        process.setnamed('::Root Element','number of samples',self.numofSamples)
        
        if(self.model=='parallel'):
            process.setnamed('DelayLine_1','length',self.DelayUnitLen)
            process.setnamed('DelayLine_2','length',(1+self.unitsNextTap)*self.DelayUnitLen)
            process.setnamed('DelayLine_3','length',(1+2*self.unitsNextTap)*self.DelayUnitLen)
            process.setnamed('DelayLine_4','length',(1+3*self.unitsNextTap)*self.DelayUnitLen)

        process.setnamed('fiber_AMP','gain',self.FiberLen*0.17e-3)
        process.setnamed('Fiber','length',self.FiberLen)
        process.setnamed('Pulse Generator','amplitude',self.PulseAmp)
        process.setnamed('PRBS','output',self.PRBSType)
        process.setnamed('Pulse Generator','rise period',self.RiseTime)
        process.setnamed('Pulse Generator','fall period',self.FallTime)
        process.setnamed('MZM','insertion loss',self.MZMILoss)

        if(self.OutputType=='disconnected'):
            for i in range(1,self.taps+1):
                process.setnamed('OutPIN_'+str(i),'enable thermal noise',self.TogglePDTNoise)
                process.setnamed('OutPIN_'+str(i),'enable shot noise',self.TogglePDSNoise)
                process.setnamed('OutPIN_'+str(i),'responsivity',self.PDResponsivity)
                process.setnamed('OutPIN_'+str(i),'dark current',self.PDDarkCurrent)
                if self.TogglePDTNoise is True: process.setnamed('OutPIN_'+str(i),'thermal noise',(self.PDTNoise)**2)
        else:
            process.setnamed('OutPIN','enable thermal noise',self.TogglePDTNoise)
            process.setnamed('OutPIN','enable shot noise',self.TogglePDSNoise)
            process.setnamed('OutPIN','responsivity',self.PDResponsivity)
            process.setnamed('OutPIN','dark current',self.PDDarkCurrent)
            if self.TogglePDTNoise is True: process.setnamed('OutPIN','thermal noise',(self.PDTNoise)**2)

        if self.ToggleAWGN is True: process.setnamed('AWGN_source','power spectral density',self.NoisePSD)
        if self.ToggleOptFilter is True: process.setnamed('Optical Filter','bandwidth',self.OptFilterBand)
                

    # Mounting section -------------------------------------------------

    def mount(self,process):
        """Method used to assembling the model in INTERCONNECT, given the attributes."""
        import numpy as np
        process.switchtolayout()
        process.deleteall()

        spacement_A = 0
        if(self.OutputType=='mixed'):
            spacement_A += 300

        process.setnamed('::Root Element','bitrate',self.bitrate)
        process.setnamed('::Root Element','time window',self.timeWindow)
        process.setnamed('::Root Element','number of samples',self.numofSamples)

        process.addelement('Optical Linear Fiber')
        process.set('x position',-600)
        process.set('y position',-200)
        process.set('length',self.FiberLen)
        process.set('attenuation',0.17e-3)
        process.set('name','Fiber')
        process.addelement('Optical Amplifier')
        process.set('enable noise',False)
        process.set('x position',-450)
        process.set('y position',-200)
        process.set('gain',self.FiberLen*0.17e-3)
        process.set('name','fiber_AMP')
        process.addelement('Optical Attenuator')
        process.set('x position',-300)
        process.set('y position',-200)
        process.set('name','VOA')
        process.addelement('Mach-Zehnder Modulator')
        process.set('x position',-750)
        process.set('y position',-200)
        process.set('modulator type','balanced single drive')
        process.set('insertion loss',self.MZMILoss)
        process.set('name','MZM')
        process.addelement('CW Laser')
        process.set('x position',-1000)
        process.set('y position',-200)
        process.set('name','CWL')
        process.addelement('NRZ Pulse Generator')
        process.set('x position',-900)
        process.set('y position',-400)
        process.set('amplitude',self.PulseAmp)
        process.set('rise period',self.RiseTime)
        process.set('fall period',self.FallTime)
        process.set('name','Pulse Generator')
        process.addelement('PRBS Generator')
        process.set('x position',-1250)
        process.set('y position',-400)
        process.set('output',self.PRBSType)
        process.set('name','PRBS')

        process.addelement('Optical Oscilloscope')
        process.set('x position',-400)
        process.set('y position',-300)
        process.addelement('Optical Oscilloscope')
        process.set('x position',-600)
        process.set('y position',-300)
        process.addelement('Optical Oscilloscope')
        process.set('x position',-225)
        process.set('y position',-300)
        process.set('name','VOA_OOSC')

        process.addelement('Oscilloscope')
        process.set('x position',-750)
        process.set('y position',-500)
        process.addelement('Logic Analyzer')
        process.set('x position',-1100)
        process.set('y position',-500)

        process.connect('CWL','output','MZM','input')
        process.connect('MZM','output','Fiber','port 1')
        process.connect('Fiber','port 2','fiber_AMP','input')
        process.connect('fiber_AMP','output','VOA','port 1')

        process.connect('Pulse Generator','output','MZM','modulation 1')

        process.connect('PRBS','output','LGCA_1','input')
        process.connect('Pulse Generator','output','OSC_1','input')
        process.connect('MZM','output','OOSC_2','input')
        process.connect('Fiber','port 2','OOSC_1','input')
        process.connect('VOA','port 2','VOA_OOSC','input')

        if self.ToggleBitOp is True:
            process.addelement('Fork 1xN')
            process.set('x position',-1050)
            process.set('y position',-415)
            process.set('number of ports',3)
            process.addelement('Data Delay')
            process.set('x position',-925)
            process.set('y position',-575)
            process.set('delay',1)
            process.addelement('Digital Logic')
            process.set('x position',-800)
            process.set('y position',-625)
            process.set('logic operator','XOR')

            process.addelement('Logic Analyzer')
            process.set('x position',-1000)
            process.set('y position',-750)
            process.addelement('Logic Analyzer')
            process.set('x position',-800)
            process.set('y position',-750)
            process.addelement('Logic Analyzer')
            process.set('x position',-650)
            process.set('y position',-750)

            process.connect('PRBS','output','FORK_1','input')
            process.connect('FORK_1','output 1','LOGIC_1','input 1')
            process.connect('FORK_1','output 2','DLY_1','input')
            process.connect('FORK_1','output 3','Pulse Generator','modulation')
            process.connect('DLY_1','output','LOGIC_1','input 2')

            process.connect('FORK_1','output 1','LGCA_2','input')
            process.connect('DLY_1','output','LGCA_3','input')
            process.connect('LOGIC_1','output','LGCA_4','input')
        else:
            process.connect('PRBS','output','Pulse Generator','modulation')

        process.addelement('Optical Oscilloscope')
        process.set('x position',350)
        process.set('y position',-500)
        process.addelement('Optical Oscilloscope')
        process.set('x position',350)
        process.set('y position',-400)
        process.addelement('Optical Oscilloscope')
        process.set('x position',350)
        process.set('y position',-200)
        process.addelement('Optical Oscilloscope')
        process.set('x position',350)
        process.set('y position',-100)

        # ----------------------------------------------------------------------------------------------------------
        # PARALLEL MODEL
        # ----------------------------------------------------------------------------------------------------------

        if(self.model=='parallel'):

            process.addelement('MZI Ideal Cell')
            process.set('x position',-100)
            process.set('y position',-300)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)
            process.set('WvgLoss',self.WvgLoss)
            process.addelement('MZI Ideal Cell')
            process.set('x position',200)
            process.set('y position',-400)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)
            process.set('WvgLoss',self.WvgLoss)
            process.addelement('MZI Ideal Cell')
            process.set('x position',200)
            process.set('y position',-200)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)
            process.set('WvgLoss',self.WvgLoss)

            process.addelement('Termination Mirror')
            process.set('x position',-200)
            process.set('y position',-100)
            process.flipelement('TERM_1')
            process.addelement('Termination Mirror')
            process.set('x position',0)
            process.set('y position',-100)
            process.flipelement('TERM_2')
            process.addelement('Termination Mirror')
            process.set('x position',0)
            process.set('y position',-500)
            process.flipelement('TERM_3')

            process.connect('IDEAL_CELL_1','port 3','IDEAL_CELL_2','port 2')
            process.connect('IDEAL_CELL_1','port 4','IDEAL_CELL_3','port 1')

            process.connect('TERM_1','port','IDEAL_CELL_1','port 2')
            process.connect('TERM_2','port','IDEAL_CELL_3','port 2')
            process.connect('TERM_3','port','IDEAL_CELL_2','port 1')

            process.setnamed('IDEAL_CELL_1','Theta 1',np.pi/2)
            process.setnamed('IDEAL_CELL_2','Theta 1',np.pi/2)
            process.setnamed('IDEAL_CELL_3','Theta 1',np.pi/2)

            process.connect('VOA','port 2','IDEAL_CELL_1','port 1')

            process.addelement('Straight Waveguide')
            process.set('x position',500)
            process.set('y position',-450)
            process.set('length',self.DelayUnitLen)
            process.set('effective index 1',2.445)
            process.set('group index 1',4.19)
            process.set('name','DelayLine_1')
            process.set('loss 1',self.WvgLoss)
            process.addelement('Straight Waveguide')
            process.set('x position',500)
            process.set('y position',-350)
            process.set('length',(1+self.unitsNextTap)*self.DelayUnitLen)
            process.set('effective index 1',2.445)
            process.set('group index 1',4.19)
            process.set('name','DelayLine_2')
            process.set('loss 1',self.WvgLoss)
            process.addelement('Straight Waveguide')
            process.set('x position',500)
            process.set('y position',-250)
            process.set('length',(1+2*self.unitsNextTap)*self.DelayUnitLen)
            process.set('effective index 1',2.445)
            process.set('group index 1',4.19)
            process.set('name','DelayLine_3')
            process.set('loss 1',self.WvgLoss)
            process.addelement('Straight Waveguide')
            process.set('x position',500)
            process.set('y position',-150)
            process.set('length',(1+3*self.unitsNextTap)*self.DelayUnitLen)
            process.set('effective index 1',2.445)
            process.set('group index 1',4.19)
            process.set('name','DelayLine_4')
            process.set('loss 1',self.WvgLoss)

            process.connect('IDEAL_CELL_2','port 3','DelayLine_1','port 1')
            process.connect('IDEAL_CELL_2','port 4','DelayLine_2','port 1')
            process.connect('IDEAL_CELL_3','port 3','DelayLine_3','port 1')
            process.connect('IDEAL_CELL_3','port 4','DelayLine_4','port 1')

            process.addelement('MZI Ideal Cell')
            process.set('x position',675)
            process.set('y position',-600)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)
            process.set('WvgLoss',self.WvgLoss)
            process.addelement('MZI Ideal Cell')
            process.set('x position',675)
            process.set('y position',-400)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)
            process.set('WvgLoss',self.WvgLoss)
            process.addelement('MZI Ideal Cell')
            process.set('x position',675)
            process.set('y position',-200)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)
            process.set('WvgLoss',self.WvgLoss)
            process.addelement('MZI Ideal Cell')
            process.set('x position',675)
            process.set('y position',0)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)
            process.set('WvgLoss',self.WvgLoss)

            process.select('OOSC_3')
            process.set('x position',925)
            process.set('y position',-600)
            process.select('OOSC_4')
            process.set('x position',925)
            process.set('y position',-400)
            process.select('OOSC_5')
            process.set('x position',925)
            process.set('y position',-200)
            process.select('OOSC_6')
            process.set('x position',925)
            process.set('y position',0)

            process.connect('DelayLine_1','port 2','IDEAL_CELL_4','port 2')
            process.connect('DelayLine_2','port 2','IDEAL_CELL_5','port 2')
            process.connect('DelayLine_3','port 2','IDEAL_CELL_6','port 2')
            process.connect('DelayLine_4','port 2','IDEAL_CELL_7','port 2')

            process.connect('IDEAL_CELL_4','port 3','OOSC_3','input')
            process.connect('IDEAL_CELL_5','port 3','OOSC_4','input')
            process.connect('IDEAL_CELL_6','port 3','OOSC_5','input')
            process.connect('IDEAL_CELL_7','port 3','OOSC_6','input')

            process.addelement('Termination Mirror')
            process.set('x position',900)
            process.set('y position',-525)
            process.addelement('Termination Mirror')
            process.set('x position',900)
            process.set('y position',-325)
            process.addelement('Termination Mirror')
            process.set('x position',900)
            process.set('y position',-125)
            process.addelement('Termination Mirror')
            process.set('x position',900)
            process.set('y position',75)

            process.connect('IDEAL_CELL_4','port 4','TERM_4','port')
            process.connect('IDEAL_CELL_5','port 4','TERM_5','port')
            process.connect('IDEAL_CELL_6','port 4','TERM_6','port')
            process.connect('IDEAL_CELL_7','port 4','TERM_7','port')

            if(self.OutputType == 'disconnected'):

                for i in range(1,self.taps+1):
                    process.addelement('PIN Photodetector')
                    process.set('x position',1000)
                    process.set('y position',-800+200*i)
                    process.set('name','OutPIN_'+str(i))
                    process.set('enable thermal noise',self.TogglePDTNoise)
                    process.set('enable shot noise',self.TogglePDSNoise)
                    process.set('responsivity',self.PDResponsivity)
                    process.set('dark current',self.PDDarkCurrent)
                    if self.TogglePDTNoise is True: process.set('thermal noise',(self.PDTNoise)**2)       

                process.connect('IDEAL_CELL_4','port 3','OutPIN_1','input')
                process.connect('IDEAL_CELL_5','port 3','OutPIN_2','input')
                process.connect('IDEAL_CELL_6','port 3','OutPIN_3','input')
                process.connect('IDEAL_CELL_7','port 3','OutPIN_4','input')

                process.addelement('Oscilloscope')
                process.set('x position',1125)
                process.set('y position',-600)
                process.addelement('Oscilloscope')
                process.set('x position',1125)
                process.set('y position',-400)
                process.addelement('Oscilloscope')
                process.set('x position',1125)
                process.set('y position',-200)
                process.addelement('Oscilloscope')
                process.set('x position',1125)
                process.set('y position',0)

                process.connect('OutPIN_1','output','OSC_2','input')
                process.connect('OutPIN_2','output','OSC_3','input')
                process.connect('OutPIN_3','output','OSC_4','input')
                process.connect('OutPIN_4','output','OSC_5','input')

            else:
                process.addelement('PIN Photodetector')
                process.set('x position',1250+spacement_A)
                process.set('y position',-300)
                process.set('name','OutPIN')
                process.set('enable thermal noise',self.TogglePDTNoise)
                process.set('enable shot noise',self.TogglePDSNoise)
                process.set('responsivity',self.PDResponsivity)
                process.set('dark current',self.PDDarkCurrent)
                if self.TogglePDTNoise is True: process.set('thermal noise',(self.PDTNoise)**2)   

                process.addelement('Oscilloscope')
                process.set('x position',1400+spacement_A)
                process.set('y position',-300)

                process.addelement('Vector Signal Analyzer')
                process.set('x position',1400+spacement_A)
                process.set('y position',200)
                process.set('name','Output_VSA')
                process.set('icon type','medium')
                process.set('configuration','single input')
                process.set('signal reference input',True)
                process.set('symbol map',True)
                process.set('calculate statistics',True)
                process.set('calculate measurements',True)

                process.connect('OutPIN','output','OSC_2','input')
                process.connect('OutPIN','output','Output_VSA','input I')
                process.connect('Pulse Generator','output','Output_VSA','reference I')

                process.addelement('Optical Splitter')
                process.set('x position',1100+spacement_A)
                process.set('y position',-300)
                process.set('configuration','combiner')
                process.set('number of ports',4)
                process.set('split ratio','none')
                process.flipelement('SPLT_1')

                process.connect('IDEAL_CELL_4','port 3','SPLT_1','input 1')
                process.connect('IDEAL_CELL_5','port 3','SPLT_1','input 2')
                process.connect('IDEAL_CELL_6','port 3','SPLT_1','input 3')
                process.connect('IDEAL_CELL_7','port 3','SPLT_1','input 4')

                if self.ToggleOptFilter is False:
                    process.connect('SPLT_1','output','OutPIN','input')
                else:
                    process.addelement('Gaussian Optical Filter')
                    process.set('x position',1200+spacement_A)
                    process.set('y position',-600)
                    process.set('name','Optical Filter')
                    process.set('bandwidth',self.OptFilterBand)
                    process.connect('SPLT_1','output','Optical Filter','input')
                    process.connect('Optical Filter','output','OutPIN','input')

                if self.ToggleAWGN is True:
                    process.addelement('Noise Source')
                    process.set('x position',1100+spacement_A)
                    process.set('y position',-100)
                    process.set('name','AWGN_source')
                    process.set('power spectral density',self.NoisePSD)

                    process.addelement('LP Gaussian Filter')
                    process.set('x position',1300+spacement_A)
                    process.set('y position',-100)
                    process.set('name','AWGN_filter')

                    process.addelement('Electrical Adder')
                    process.set('x position',1500+spacement_A)
                    process.set('y position',-200)
                    process.set('name','Output_sum')

                    process.addelement('Oscilloscope')
                    process.set('x position',1600+spacement_A)
                    process.set('y position',-250)
                    process.addelement('Power Meter')
                    process.set('x position',1600+spacement_A)
                    process.set('y position',-350)
                    process.set('name','Signal_Power')
                    process.addelement('Power Meter')
                    process.set('x position',1600+spacement_A)
                    process.set('y position',-100)
                    process.set('name','Noise_Power')

                    process.connect('AWGN_source','output','AWGN_filter','input')
                    process.connect('OutPIN','output','Output_sum','input 1')
                    process.connect('OutPIN','output','Signal_Power','input')
                    process.connect('AWGN_filter','output','Output_sum','input 2')
                    process.connect('AWGN_filter','output','Noise_Power','input')
                    process.connect('Output_sum','output','OSC_3','input')

                if(self.OutputType=='mixed'):

                    process.disconnect('IDEAL_CELL_4','port 3','SPLT_1','input 1')
                    process.disconnect('IDEAL_CELL_5','port 3','SPLT_1','input 2')
                    process.disconnect('IDEAL_CELL_6','port 3','SPLT_1','input 3')
                    process.disconnect('IDEAL_CELL_7','port 3','SPLT_1','input 4')

                    process.addelement('Optical Splitter')
                    process.set('x position',1025)
                    process.set('y position',-600)
                    process.set('configuration','splitter')
                    process.set('number of ports',2)
                    process.set('split ratio','none')
                    process.set('name','arm1_splt')
                    process.addelement('Optical Splitter')
                    process.set('x position',1025)
                    process.set('y position',-400)
                    process.set('configuration','splitter')
                    process.set('number of ports',2)
                    process.set('split ratio','none')
                    process.set('name','arm2_splt')
                    process.addelement('Optical Splitter')
                    process.set('x position',1025)
                    process.set('y position',-200)
                    process.set('configuration','splitter')
                    process.set('number of ports',2)
                    process.set('split ratio','none')
                    process.set('name','arm3_splt')
                    process.addelement('Optical Splitter')
                    process.set('x position',1025)
                    process.set('y position',0)
                    process.set('configuration','splitter')
                    process.set('number of ports',2)
                    process.set('split ratio','none')
                    process.set('name','arm4_splt')

                    process.connect('IDEAL_CELL_4','port 3','arm1_splt','input')
                    process.connect('IDEAL_CELL_5','port 3','arm2_splt','input')
                    process.connect('IDEAL_CELL_6','port 3','arm3_splt','input')
                    process.connect('IDEAL_CELL_7','port 3','arm4_splt','input')

                    process.connect('arm1_splt','output 2','SPLT_1','input 1')
                    process.connect('arm2_splt','output 2','SPLT_1','input 2')
                    process.connect('arm3_splt','output 2','SPLT_1','input 3')
                    process.connect('arm4_splt','output 2','SPLT_1','input 4')

                    process.addelement('PIN Photodetector')
                    process.set('x position',1175)
                    process.set('y position',-600)
                    process.set('enable thermal noise',0)
                    process.set('enable shot noise',0)
                    process.set('name','arm1_pin')
                    process.addelement('PIN Photodetector')
                    process.set('x position',1175)
                    process.set('y position',-400)
                    process.set('enable thermal noise',0)
                    process.set('enable shot noise',0)
                    process.set('name','arm2_pin')
                    process.addelement('PIN Photodetector')
                    process.set('x position',1175)
                    process.set('y position',-200)
                    process.set('enable thermal noise',0)
                    process.set('enable shot noise',0)
                    process.set('name','arm3_pin')
                    process.addelement('PIN Photodetector')
                    process.set('x position',1175)
                    process.set('y position',0)
                    process.set('enable thermal noise',0)
                    process.set('enable shot noise',0)
                    process.set('name','arm4_pin')

                    process.addelement('Oscilloscope')
                    process.set('x position',1300)
                    process.set('y position',-650)
                    process.set('name','arm1_osc')
                    process.addelement('Oscilloscope')
                    process.set('x position',1300)
                    process.set('y position',-450)
                    process.set('name','arm2_osc')
                    process.addelement('Oscilloscope')
                    process.set('x position',1300)
                    process.set('y position',-250)
                    process.set('name','arm3_osc')
                    process.addelement('Oscilloscope')
                    process.set('x position',1300)
                    process.set('y position',-50)
                    process.set('name','arm4_osc')

                    process.connect('arm1_splt','output 1','arm1_pin','input')
                    process.connect('arm2_splt','output 1','arm2_pin','input')
                    process.connect('arm3_splt','output 1','arm3_pin','input')
                    process.connect('arm4_splt','output 1','arm4_pin','input')

                    process.connect('arm1_pin','output','arm1_osc','input')
                    process.connect('arm2_pin','output','arm2_osc','input')
                    process.connect('arm3_pin','output','arm3_osc','input')
                    process.connect('arm4_pin','output','arm4_osc','input')

        # ----------------------------------------------------------------------------------------------------------
        # SERIES MODEL
        # ----------------------------------------------------------------------------------------------------------

        elif(self.model=='series'):

            process.addelement('Straight Waveguide')
            process.set('x position',-125)
            process.set('y position',-500)
            process.set('length',self.DelayUnitLen)
            process.set('effective index 1',2.445)
            process.set('group index 1',4.19)
            process.addelement('Straight Waveguide')
            process.set('x position',-50)
            process.set('y position',-300)
            process.set('length',self.DelayUnitLen)
            process.set('effective index 1',2.445)
            process.set('group index 1',4.19)
            process.addelement('Straight Waveguide')
            process.set('x position',25)
            process.set('y position',-100)
            process.set('length',2*self.DelayUnitLen)
            process.set('effective index 1',2.445)
            process.set('group index 1',4.19)

            process.addelement('MZI Ideal Cell')
            process.set('x position',175)
            process.set('y position',-600)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)
            process.addelement('MZI Ideal Cell')
            process.set('x position',175)
            process.set('y position',-400)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)
            process.addelement('MZI Ideal Cell')
            process.set('x position',175)
            process.set('y position',-200)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)
            process.addelement('MZI Ideal Cell')
            process.set('x position',175)
            process.set('y position',0)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)

            process.select('OOSC_3')
            process.set('x position',450)
            process.set('y position',-600)
            process.select('OOSC_4')
            process.set('x position',450)
            process.set('y position',-400)
            process.select('OOSC_5')
            process.set('x position',450)
            process.set('y position',-200)
            process.select('OOSC_6')
            process.set('x position',450)
            process.set('y position',0)

            process.connect('IDEAL_CELL_1','port 3','OOSC_3','input')
            process.connect('IDEAL_CELL_2','port 3','OOSC_4','input')
            process.connect('IDEAL_CELL_3','port 3','OOSC_5','input')
            process.connect('IDEAL_CELL_4','port 3','OOSC_6','input')


            process.addelement('MZI Ideal Cell')
            process.set('x position',-375)
            process.set('y position',-600)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)
            process.addelement('MZI Ideal Cell')
            process.set('x position',-300)
            process.set('y position',-400)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)
            process.addelement('MZI Ideal Cell')
            process.set('x position',-225)
            process.set('y position',-200)
            process.set('Waveguide neff',2.445)
            process.set('Waveguide ng',4.19)

            process.setnamed('IDEAL_CELL_5','Theta 1',1.335*np.pi/4)
            process.setnamed('IDEAL_CELL_6','Theta 1',1.57*np.pi/4)
            process.setnamed('IDEAL_CELL_7','Theta 1',np.pi/2)

            process.connect('VOA','port 2','IDEAL_CELL_5','port 1')

            process.connect('IDEAL_CELL_5','port 4','WGD_1','port 1')
            process.connect('IDEAL_CELL_6','port 4','WGD_2','port 1')
            process.connect('IDEAL_CELL_7','port 4','WGD_3','port 1')

            process.connect('IDEAL_CELL_5','port 3','IDEAL_CELL_1','port 2')
            process.connect('IDEAL_CELL_6','port 3','IDEAL_CELL_2','port 2')
            process.connect('IDEAL_CELL_7','port 3','IDEAL_CELL_3','port 2')

            process.connect('WGD_1','port 2','IDEAL_CELL_6','port 1')
            process.connect('WGD_2','port 2','IDEAL_CELL_7','port 1')
            process.connect('WGD_3','port 2','IDEAL_CELL_4','port 2')

            process.addelement('PIN Photodetector')
            process.set('x position',600)
            process.set('y position',-600)
            process.set('enable thermal noise',0)
            process.set('enable shot noise',0)
            process.addelement('PIN Photodetector')
            process.set('x position',600)
            process.set('y position',-400)
            process.set('enable thermal noise',0)
            process.set('enable shot noise',0)
            process.addelement('PIN Photodetector')
            process.set('x position',600)
            process.set('y position',-200)
            process.set('enable thermal noise',0)
            process.set('enable shot noise',0)
            process.addelement('PIN Photodetector')
            process.set('x position',600)
            process.set('y position',0)
            process.set('enable thermal noise',0)
            process.set('enable shot noise',0)

            process.connect('IDEAL_CELL_1','port 3','PIN_1','input')
            process.connect('IDEAL_CELL_2','port 3','PIN_2','input')
            process.connect('IDEAL_CELL_3','port 3','PIN_3','input')
            process.connect('IDEAL_CELL_4','port 3','PIN_4','input')

            process.addelement('Oscilloscope')
            process.set('x position',725)
            process.set('y position',-600)
            process.addelement('Oscilloscope')
            process.set('x position',725)
            process.set('y position',-400)
            process.addelement('Oscilloscope')
            process.set('x position',725)
            process.set('y position',-200)
            process.addelement('Oscilloscope')
            process.set('x position',725)
            process.set('y position',0)

            process.connect('PIN_1','output','OSC_2','input')
            process.connect('PIN_2','output','OSC_3','input')
            process.connect('PIN_3','output','OSC_4','input')
            process.connect('PIN_4','output','OSC_5','input')