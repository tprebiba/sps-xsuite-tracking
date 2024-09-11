/**
 * 
 */
package cern.accsoft.steering.jmad.modeldefs.defs.tt10sps;

import cern.accsoft.steering.jmad.domain.file.CallableModelFileImpl;
import cern.accsoft.steering.jmad.domain.file.ModelFile;
import cern.accsoft.steering.jmad.domain.file.ModelPathOffsetsImpl;
import cern.accsoft.steering.jmad.domain.file.CallableModelFile.ParseType;
import cern.accsoft.steering.jmad.domain.file.ModelFile.ModelFileLocation;
import cern.accsoft.steering.jmad.domain.machine.MadxRange;
import cern.accsoft.steering.jmad.domain.machine.RangeDefinitionImpl;
import cern.accsoft.steering.jmad.domain.machine.SequenceDefinitionImpl;
import cern.accsoft.steering.jmad.domain.machine.filter.RegexNameFilter;
import cern.accsoft.steering.jmad.domain.result.tfs.TfsResult;
import cern.accsoft.steering.jmad.domain.twiss.TwissInitialConditionsImpl;
import cern.accsoft.steering.jmad.domain.types.enums.JMadPlane;
import cern.accsoft.steering.jmad.factory.BeamFactory;
import cern.accsoft.steering.jmad.modeldefs.ModelDefinitionFactory;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinitionImpl;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinitionImpl;

/**
 * This class is the actual model configuration for the TT2TT10SPS transfer line for Ions.
 * 
 * @author F.M. Velotti copied from Kajetan Fuchsberger implementation
 */
public class TT10spsIonsNewStrnModelDefinitionFactory implements ModelDefinitionFactory {

    @Override
    public JMadModelDefinition create() {
        JMadModelDefinitionImpl modelDefinition = new JMadModelDefinitionImpl();
        modelDefinition.setName("PB81NFOILTT10SPS");

        ModelPathOffsetsImpl offsets = new ModelPathOffsetsImpl();
        offsets.setResourceOffset("tt10sps/2016");
        modelDefinition.setModelPathOffsets(offsets);

        modelDefinition.addInitFile(new CallableModelFileImpl("beam/lhc_beam_inj.madx", ModelFileLocation.RESOURCE));
        modelDefinition.addInitFile(new CallableModelFileImpl("sequence/tt10sps.seq", ModelFileLocation.RESOURCE));

        /*
         * OPTICS
         */
        String[] strengthFileNames = new String[] { 
                "str/tt10_sps_new_strn2_pb80-81-2018.str"
               };
        

        for (String strengthFileName : strengthFileNames) {
            String opticsName = strengthFileName.replaceAll("str/tt10_sps_", "SPSInjection-").replace(".str", "");
            OpticsDefinition opticsDefinition = new OpticsDefinitionImpl(opticsName,
                    new ModelFile[] { new CallableModelFileImpl(strengthFileName, ModelFileLocation.RESOURCE,
                            ParseType.STRENGTHS) });
            modelDefinition.addOpticsDefinition(opticsDefinition);
        }
        modelDefinition.setDefaultOpticsDefinition(modelDefinition.getOpticsDefinitions().get(0));

        /*
         * SEQUENCE
         * This works for JMAD but not for the optics uploader...
         * MadxRange range = new MadxRange("strn", "#e");
         */

       
        SequenceDefinitionImpl tt10sps = new SequenceDefinitionImpl("tt2tt10sps",null);
        modelDefinition.setDefaultSequenceDefinition(tt10sps);
        
        
        RangeDefinitionImpl tt10spsrange = new RangeDefinitionImpl(tt10sps, "ALL", createTT10InitialConditions());
        tt10sps.setDefaultRangeDefinition(tt10spsrange);

        return modelDefinition;
    }

    /**
     * Twiss initial conditions for transferline TT2 after strn1
     */
    private final TwissInitialConditionsImpl createTT10InitialConditions() {
        TwissInitialConditionsImpl twissInitialConditions = new TwissInitialConditionsImpl("tt10sps-twiss");

        /** 
         * !  twiss parameters at beginning of TT2 for Pb ions @ 26 GeV/c
            !
            !
            ! Considering Twiss parameters change due to back-scattering at stripper
            ! New optics 10/10/2007 (G.Arduini, E.Benedetto, M.Martini)
            ! based on measurements of 20th Sept '07
            !
            
            BETX0  := 32.738; 
            ALFX0  := -3.074;  
            BETY0  := 10.561;  
            ALFY0  :=  0.706; 
            DX0    :=  3.097; 
            DPX0   :=  0.250; 
            DY0    :=  0.301; 
            DPY0   :=  0.018; 
            MUX0   :=  0.000000000000;
            MUY0   :=  0.000000000000;
            X0     :=  0.000000000000;
            PX0    :=  0.000000000000;
            Y0     :=  0.000000000000;
            PY0    :=  0.000000000000;
            T0     :=  0.000000000000;
            PT0    :=  0.000000000000;
         * 
        ***/

        twissInitialConditions.setDeltap(0.0);
        twissInitialConditions.setBetx(32.738);
        twissInitialConditions.setAlfx(-3.074);
        twissInitialConditions.setDx(3.097);
        twissInitialConditions.setDpx(0.250);
        twissInitialConditions.setBety(10.561);
        twissInitialConditions.setAlfy(0.706);
        twissInitialConditions.setDy(0.301);
        twissInitialConditions.setDpy(0.018);
        twissInitialConditions.setCalcAtCenter(true);
        twissInitialConditions.setClosedOrbit(false);
        return twissInitialConditions;

    }

}
