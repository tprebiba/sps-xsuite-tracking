/**
 * 
 */
package cern.accsoft.steering.jmad.modeldefs.defs.tt66;

import cern.accsoft.steering.jmad.domain.file.CallableModelFileImpl;
import cern.accsoft.steering.jmad.domain.file.ModelFile;
import cern.accsoft.steering.jmad.domain.file.ModelPathOffsetsImpl;
import cern.accsoft.steering.jmad.domain.file.CallableModelFile.ParseType;
import cern.accsoft.steering.jmad.domain.file.ModelFile.ModelFileLocation;
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
 * This class is the actual model configuration for the TI2 transfer line.
 * 
 * @author Kajetan Fuchsberger (kajetan.fuchsberger at cern.ch)
 */
public class Tt66ModelDefinitionFactory implements ModelDefinitionFactory {

    @Override
    public JMadModelDefinition create() {
        JMadModelDefinitionImpl modelDefinition = new JMadModelDefinitionImpl();
        modelDefinition.setName("TT66");

        ModelPathOffsetsImpl offsets = new ModelPathOffsetsImpl();
        offsets.setResourceOffset("tt66/2014");
        modelDefinition.setModelPathOffsets(offsets);

        modelDefinition.addInitFile(new CallableModelFileImpl("beam/beam.madx", ModelFileLocation.RESOURCE));
        modelDefinition.addInitFile(new CallableModelFileImpl("sequence/tt66-v11.seq", ModelFileLocation.RESOURCE));

        /*
         * OPTICS
         */
        String[] strengthFileNames = new String[] {
                "str/my_fp1_0p1mm.str",
                "str/my_fp1_0p2mm.str",
                "str/my_fp1_0p5mm.str",
                "str/my_fp1_0p7mm.str",
                "str/my_fp1_1p0mm.str",
                "str/my_fp1_2p0mm.str",               
                "str/my_fp1_2p5mm.str",
                "str/my_fp1_3p0mm.str",
                "str/my_fp1_3p5mm.str",
                "str/my_fp1_4p0mm.str",               
                "str/my_fp2_0p1mm.str",
                "str/my_fp2_0p2mm.str",
                "str/my_fp2_0p25mm.str",
                "str/my_fp2_0p3mm.str",
                "str/my_fp2_0p5mm.str",
                "str/my_fp2_0p7mm.str",
                "str/my_fp2_1p0mm.str",
                "str/my_fp2_1p5mm.str",
                "str/my_fp2_2p0mm.str",               
                "str/my_fp2_2p5mm.str",
                "str/my_fp2_3p0mm.str",
                "str/my_fp2_3p5mm.str",
                "str/my_fp2_4p0mm.str",           
                "str/my_fp3_0p1mm.str",
                "str/my_fp3_0p2mm.str",
                "str/my_fp3_0p5mm.str",
                "str/my_fp3_0p7mm.str",
                "str/my_fp3_1p0mm.str",
                "str/my_fp3_1p5mm.str",
                "str/my_fp3_2p0mm.str",
                "str/my_fp3_2p5mm.str",
                "str/my_fp3_3p0mm.str",
                "str/my_fp3_3p5mm.str",
                "str/my_fp3_4p0mm.str",              
                "str/my_fp1_10p0mm.str"};
        

        for (String strengthFileName : strengthFileNames) {
            String opticsName = strengthFileName.replaceAll("str/my_", "tt66_2014_").replaceAll(".str", "");
            OpticsDefinition opticsDefinition = new OpticsDefinitionImpl(opticsName,
                    new ModelFile[] { new CallableModelFileImpl(strengthFileName, ModelFileLocation.RESOURCE,
                            ParseType.STRENGTHS) });
            modelDefinition.addOpticsDefinition(opticsDefinition);
        }
        modelDefinition.setDefaultOpticsDefinition(modelDefinition.getOpticsDefinitions().get(0));

        /*
         * SEQUENCE
         */

       
        SequenceDefinitionImpl tt66 = new SequenceDefinitionImpl("tt66",null);
        modelDefinition.setDefaultSequenceDefinition(tt66);
        RangeDefinitionImpl tt66range = new RangeDefinitionImpl(tt66, "ALL", createT66InitialConditions());
        tt66.setDefaultRangeDefinition(tt66range);

        return modelDefinition;
    }

    /**
     * Twiss initial conditions for transferline T66
     */
    private final TwissInitialConditionsImpl createT66InitialConditions() {
        TwissInitialConditionsImpl twissInitialConditions = new TwissInitialConditionsImpl("tt66-twiss");

        twissInitialConditions.setDeltap(0.0);
        twissInitialConditions.setBetx(27.77906807);
        twissInitialConditions.setAlfx(0.63611880);
        twissInitialConditions.setDx(-0.59866300);
        twissInitialConditions.setDpx(0.01603536);
        twissInitialConditions.setBety(120.39920690);
        twissInitialConditions.setAlfy(-2.70621900);
        twissInitialConditions.setDy(0.0);
        twissInitialConditions.setDpy(0.0);
        twissInitialConditions.setCalcAtCenter(true);
        twissInitialConditions.setClosedOrbit(false);
        return twissInitialConditions;

    }

}
